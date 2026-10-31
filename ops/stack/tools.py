"""Operator commands and acceptance against the running self-hosted services."""

import asyncio
import hashlib
import json
import logging
import os
from pathlib import Path
import ssl
import sys
import time
from uuid import uuid4

import httpx2 as httpx

logging.basicConfig(level=logging.WARNING)
os.environ.update(json.loads(Path('/run/lab/runtime.json').read_text()))
CREDENTIALS = json.loads(Path('/run/operator/credentials.json').read_text())
TLS = ssl.create_default_context(cafile='/run/lab/ca.crt')
BASE = 'https://keycloak:8443/realms/supportops/protocol/openid-connect'
AGENT_SCOPES = 'ticket:read ticket:write task:read task:write triage:run billing:read crm:read refund:request feedback:write'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def token(client, username='agent-a'):
    key = {'agent-a':'agent_a','agent-b':'agent_b','approver-a':'approver_a'}[username]
    scope = 'ticket:read task:read approval:decide' if username=='approver-a' else AGENT_SCOPES
    response = client.post(BASE+'/token',data={
        'grant_type':'password','client_id':'supportops-api','client_secret':CREDENTIALS['client_secret'],
        'username':username,'password':CREDENTIALS[key],'scope':scope,
    })
    require(response.status_code==200, f'Keycloak token request failed with HTTP {response.status_code}')
    return response.json()['access_token']


def wait_task(client, url, headers, wanted, seconds=90):
    deadline = time.monotonic()+seconds
    while time.monotonic()<deadline:
        response = client.get(url,headers=headers)
        require(response.status_code==200,f'Task lookup failed with HTTP {response.status_code}')
        task = response.json()
        if task['status']==wanted:
            return task
        require(task['status']!='failed','Worker task failed; inspect the scoped Compose worker logs')
        time.sleep(1)
    raise RuntimeError('Worker task did not reach '+wanted)


async def mcp_call(access_token, invoice='inv-a-1'):
    from mcp.client.session import ClientSession
    from mcp.client.streamable_http import streamable_http_client
    async with httpx.AsyncClient(headers={'Authorization':'Bearer '+access_token},timeout=15,verify=TLS) as client:
        async with streamable_http_client('http://mcp:8000/mcp',http_client=client) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                return await session.call_tool('lookup_invoice',{'invoice_id':invoice})


def check():
    from supportops_platform.rag.postgres import PostgresRetriever
    from supportops_platform.rag.retrieval import KnowledgeDocument
    retriever=PostgresRetriever(os.environ['P05_POSTGRES_DSN'])
    retriever.ingest(KnowledgeDocument('lab-invoice-policy','tenant-a','Invoice policy',
                                    'Verify the invoice charge before responding. Refund requires human approval.'))
    with httpx.Client(verify=TLS,timeout=20) as client:
        discovery=client.get('https://keycloak:8443/realms/supportops/.well-known/openid-configuration')
        require(discovery.status_code==200,'Keycloak HTTPS discovery is unavailable')
        require(discovery.json()['issuer']==os.environ['LAB_IDP_URL']+'/realms/supportops','Issuer URL mismatch')
        own_token,foreign_token=token(client),token(client,'agent-b')
        own={'Authorization':'Bearer '+own_token}
        foreign={'Authorization':'Bearer '+foreign_token}
        require(client.get('http://api:8000/v1/tickets').status_code==401,'API accepted a missing bearer')
        created=client.post('http://api:8000/v1/tickets',headers=own,json={
            'customer_id':'customer-a','subject':'Invoice charge question','body':'Please explain the invoice policy.',
        })
        require(created.status_code==201,f'Ticket creation failed with HTTP {created.status_code}')
        ticket=created.json()['id']
        require(client.get('http://api:8000/v1/tickets/'+ticket,headers=foreign).status_code==404,'Cross-tenant ticket exposed')
        submitted=client.post('http://api:8000/v1/tasks',headers={**own,'Idempotency-Key':uuid4().hex},json={'ticket_id':ticket})
        require(submitted.status_code==202,f'P05 submission failed with HTTP {submitted.status_code}')
        p05_task=submitted.json()['id']
        result=wait_task(client,'http://api:8000/v1/tasks/'+p05_task,own,'succeeded')
        require(result['result']['citations'],'P05 worker did not return tenant knowledge citations')
        print('PASS P05: OIDC API -> durable queue -> P01 agent -> pgvector RAG -> signed MCP -> persisted result',flush=True)
        require(not asyncio.run(mcp_call(own_token)).is_error,'External OIDC MCP access failed')
        require(asyncio.run(mcp_call(foreign_token)).is_error,'MCP exposed tenant-A invoice to tenant B')
        print('PASS tenant isolation: API denies cross-tenant ticket; MCP denies cross-tenant invoice',flush=True)

        refund_ticket=client.post('http://api:8000/v1/tickets',headers=own,json={
            'customer_id':'customer-a','subject':'Refund invoice request','body':'Please review my invoice refund.',
        })
        require(refund_ticket.status_code==201,'Refund ticket creation failed')
        refund=client.post('http://api:8000/v1/tasks',headers={**own,'Idempotency-Key':uuid4().hex},
                           json={'ticket_id':refund_ticket.json()['id']})
        require(refund.status_code==202,'Refund task submission failed')
        paused=wait_task(client,'http://api:8000/v1/tasks/'+refund.json()['id'],own,'needs_approval')
        approval_url='http://api:8000/v1/tickets/'+refund_ticket.json()['id']+'/approve'
        approval={'approval_id':paused['result']['approval_id']}
        require(client.post(approval_url,headers=own,json=approval).status_code==403,'Requester approved own refund')
        approver={'Authorization':'Bearer '+token(client,'approver-a')}
        require(client.post(approval_url,headers=approver,json=approval).status_code==200,'Independent approval failed')
        final=wait_task(client,'http://api:8000/v1/tasks/'+refund.json()['id'],own,'succeeded')
        require(final['result']['refund']['simulated'] is True,'Approved fake effect was not recorded')
        print('PASS HITL: separate OIDC approver resumes the original bounded authorization snapshot',flush=True)

        require(client.get('http://web:8080/healthz').status_code==200,'Console is not serving')
        require(client.get('http://web:8080/readyz').status_code==200,'Console cannot reach P05')
        proxied=client.get('http://web:8080/api/v1/tickets',headers=own)
        require(proxied.status_code==200,f'Console API proxy failed with HTTP {proxied.status_code}')
        require('default-src' in client.get('http://web:8080/').headers.get('content-security-policy',''),'Console served no CSP')
        grant=client.post(BASE+'/token',data={'grant_type':'password','client_id':'supportops-web','username':'agent-a','password':CREDENTIALS['agent_a']})
        require(grant.status_code==400,'Public console client accepted the password grant')
        trace_id=uuid4().hex
        traced=client.get('http://web:8080/api/v1/tickets',headers={**own,'traceparent':f'00-{trace_id}-{uuid4().hex[:16]}-01'})
        require(traced.headers.get('x-trace-id')==trace_id,'Browser traceparent did not reach P05')
        print('PASS console: health, P05 proxy, CSP, PKCE-only public client and browser trace propagation',flush=True)

        p04=client.post('http://p04-api:8000/tasks',headers={'Idempotency-Key':uuid4().hex},
                        json={'payload':{'ticket_id':'lab-stack-demo'},'steps':['triage','draft_reply']})
        require(p04.status_code==202,'P04 submission failed')
        p04_task=p04.json()['task_id']
        wait_task(client,'http://p04-api:8000/tasks/'+p04_task,{},'done')
        print('PASS P04: independent API, PostgreSQL store, Redis Streams and worker',flush=True)

        response=client.post(BASE+'/revoke',data={'client_id':'supportops-api','client_secret':CREDENTIALS['client_secret'],
                                                 'token':own_token,'token_type_hint':'access_token'})
        require(response.status_code==200,'Keycloak token revocation failed')
        deadline=time.monotonic()+15
        while time.monotonic()<deadline:
            if client.get('http://api:8000/v1/tickets',headers=own).status_code==401:
                break
            time.sleep(0.5)
        else:
            raise RuntimeError('API continued accepting the revoked token')
        denied=client.post('http://mcp:8000/mcp',headers={**own,'Accept':'application/json, text/event-stream'},json={
            'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25',
             'capabilities':{},'clientInfo':{'name':'lab-acceptance','version':'1'}},
        })
        require(denied.status_code==401,'MCP continued accepting the revoked token')
        print('PASS persistent self-hosted Keycloak: issued token, verified HTTPS introspection, API/MCP revocation denial',flush=True)

        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            targets=client.get('http://prometheus:9090/api/v1/targets').json()['data']['activeTargets']
            if len(targets)>=2 and all(t['health']=='up' for t in targets):
                break
            time.sleep(1)
        else:
            raise RuntimeError('Prometheus did not observe healthy API and worker targets')
        dashboards=client.get('http://grafana:3000/api/search',auth=('lab-admin',CREDENTIALS['grafana']))
        require(dashboards.status_code==200 and dashboards.json(),'Grafana provisioning unavailable')
        trace_id=submitted.headers.get('X-Trace-ID')
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            traces=client.get('http://jaeger:16686/api/traces/'+trace_id).json().get('data',[])
            names={span['operationName'] for item in traces for span in item['spans']}
            if {'api.request','worker.run','agent.triage','mcp.request'}<=names:
                break
            time.sleep(1)
        else:
            raise RuntimeError('Jaeger did not expose the correlated product trace')
        print('PASS P03: healthy metric targets, provisioned dashboards and correlated API/worker/MCP trace',flush=True)
        marker={'ticket':ticket,'p05_task':p05_task,'p04_task':p04_task,
                'ca_sha256':hashlib.sha256(Path('/run/lab/ca.crt').read_bytes()).hexdigest()}
        Path('/run/acceptance/acceptance.json').write_text(json.dumps(marker))
        print('ACCEPTANCE PASS; LLM_MODE=fake; model quality PENDING',flush=True)


def persistence():
    marker=json.loads(Path('/run/acceptance/acceptance.json').read_text())
    require(hashlib.sha256(Path('/run/lab/ca.crt').read_bytes()).hexdigest()==marker['ca_sha256'],'CA unexpectedly rotated')
    with httpx.Client(verify=TLS,timeout=20) as client:
        own={'Authorization':'Bearer '+token(client)}
        require(client.get('http://api:8000/v1/tickets/'+marker['ticket'],headers=own).status_code==200,'P05 ticket lost')
        wait_task(client,'http://api:8000/v1/tasks/'+marker['p05_task'],own,'succeeded')
        wait_task(client,'http://p04-api:8000/tasks/'+marker['p04_task'],{},'done')
    print('PERSISTENCE PASS: same credentials/CA, Keycloak realm/users, P04 and P05 completed records survived container recreation.')


def main():
    action=sys.argv[1] if len(sys.argv)>1 else 'check'
    if action=='credentials':
        for label,key in [('Keycloak lab-admin','keycloak_admin'),('Grafana lab-admin','grafana'),
                          ('agent-a','agent_a'),('agent-b','agent_b'),('approver-a','approver_a')]:
            print(label+': '+CREDENTIALS[key])
    elif action=='ca':
        print(Path('/run/lab/ca.crt').read_text(),end='')
    elif action=='token':
        with httpx.Client(verify=TLS,timeout=20) as client:
            print(token(client,sys.argv[2] if len(sys.argv)>2 else 'agent-a'))
    elif action=='persistence':
        persistence()
    elif action=='check':
        check()
    else:
        raise ValueError('Unknown operator command')


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('STACK CHECK FAILED: '+type(exc).__name__+': '+str(exc),file=sys.stderr)
        raise SystemExit(1)
