"""Apply the browser OIDC client through the Keycloak admin API, idempotently.

--import-realm skips a realm that already exists, so editing the realm file
would never reach a running volume or the deployed Fly realm.
"""

import json
import os
from pathlib import Path
import ssl
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

REALM = 'supportops'
CLIENT_ID = 'supportops-web'
SCOPES = ('ticket:read', 'ticket:write', 'task:read', 'task:write', 'triage:run',
          'refund:request', 'feedback:write', 'approval:decide', 'billing:read', 'crm:read')


def claim(name, config):
    return {'name': name, 'protocol': 'openid-connect', 'protocolMapper': config.pop('mapper'),
            'config': {'access.token.claim': 'true', 'introspection.token.claim': 'true', **config}}


def client_document(origin):
    return {
        'clientId': CLIENT_ID, 'name': 'SupportOps Console', 'enabled': True, 'protocol': 'openid-connect',
        'publicClient': True, 'standardFlowEnabled': True, 'directAccessGrantsEnabled': False,
        'implicitFlowEnabled': False, 'serviceAccountsEnabled': False, 'fullScopeAllowed': True,
        'rootUrl': origin, 'redirectUris': [origin + '/'], 'webOrigins': [origin],
        'attributes': {'pkce.code.challenge.method': 'S256', 'post.logout.redirect.uris': origin + '/'},
        'protocolMappers': [
            claim('tenant', {'mapper': 'oidc-usermodel-attribute-mapper', 'user.attribute': 'tenant_id',
                             'claim.name': 'tenant_id', 'jsonType.label': 'String'}),
            claim('roles', {'mapper': 'oidc-usermodel-realm-role-mapper', 'claim.name': 'roles',
                            'multivalued': 'true', 'user.realmRole': 'true'}),
            claim('audience', {'mapper': 'oidc-audience-mapper', 'included.client.audience': 'supportops-api'}),
            claim('username', {'mapper': 'oidc-usermodel-property-mapper', 'user.attribute': 'username',
                               'claim.name': 'preferred_username', 'jsonType.label': 'String'}),
        ],
    }


class Admin:
    def __init__(self, base, password, context):
        self.base = base.rstrip('/')
        self.context = context
        body = urlencode({'grant_type': 'password', 'client_id': 'admin-cli',
                          'username': os.environ.get('IDP_ADMIN_USER', 'lab-admin'), 'password': password})
        request = Request(self.base + '/realms/master/protocol/openid-connect/token', data=body.encode(),
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urlopen(request, context=context, timeout=15) as response:
            self.token = json.load(response)['access_token']

    def call(self, method, path, document=None):
        data = None if document is None else json.dumps(document).encode()
        request = Request(f'{self.base}/admin/realms/{REALM}{path}', data=data, method=method,
                          headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'})
        with urlopen(request, context=self.context, timeout=15) as response:
            raw = response.read()
        return json.loads(raw) if raw else None


def apply_client(admin, origin):
    wanted = client_document(origin)
    found = admin.call('GET', f'/clients?clientId={CLIENT_ID}')
    if found:
        client = found[0]['id']
        mappers = {item['name']: item['id'] for item in admin.call('GET', f'/clients/{client}/protocol-mappers/models')}
        for mapper in wanted['protocolMappers']:
            if mapper['name'] in mappers:
                mapper['id'] = mappers[mapper['name']]
                admin.call('PUT', f"/clients/{client}/protocol-mappers/models/{mapper['id']}", mapper)
            else:
                admin.call('POST', f'/clients/{client}/protocol-mappers/models', mapper)
        update = {key: value for key, value in wanted.items() if key != 'protocolMappers'}
        admin.call('PUT', f'/clients/{client}', {**found[0], **update})
    else:
        admin.call('POST', '/clients', wanted)
        client = admin.call('GET', f'/clients?clientId={CLIENT_ID}')[0]['id']
    available = {item['name']: item['id'] for item in admin.call('GET', '/client-scopes')}
    missing = [scope for scope in SCOPES if scope not in available]
    if missing:
        raise RuntimeError('realm is missing client scopes: ' + ', '.join(missing))
    for scope in SCOPES:
        admin.call('PUT', f'/clients/{client}/optional-client-scopes/{quote(available[scope], safe="")}')


def main():
    origin = os.environ['WEB_ORIGIN'].rstrip('/')
    ca_file = os.environ.get('IDP_CA_FILE')
    context = ssl.create_default_context(cafile=ca_file) if ca_file else ssl.create_default_context()
    credentials_file = os.environ.get('IDP_CREDENTIALS_FILE')
    password = (json.loads(Path(credentials_file).read_text())['keycloak_admin'] if credentials_file
                else os.environ['IDP_ADMIN_PASSWORD'])
    deadline = time.monotonic() + 120
    while True:
        try:
            admin = Admin(os.environ['IDP_URL'], password, context)
            break
        except (URLError, HTTPError) as error:
            if time.monotonic() > deadline:
                print(f'Keycloak admin login failed: {error}', file=sys.stderr)
                return 1
            time.sleep(3)
    apply_client(admin, origin)
    print(f'Applied OIDC client {CLIENT_ID} for {origin}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
