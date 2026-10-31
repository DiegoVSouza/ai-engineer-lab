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
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

REALM = 'supportops'
CLIENT_ID = 'supportops-web'
SCOPES = ('ticket:read', 'ticket:write', 'task:read', 'task:write', 'triage:run',
          'refund:request', 'feedback:write', 'approval:decide', 'billing:read', 'crm:read')


def claim(name, config):
    return {'name': name, 'protocol': 'openid-connect', 'protocolMapper': config.pop('mapper'),
            'config': {'access.token.claim': 'true', 'introspection.token.claim': 'true', **config}}


LOOPBACK = {'localhost', '127.0.0.1', '[::1]'}


def parse_origins(value):
    """Comma-separated front origins: exact https, or loopback http. No wildcard, path or empty list."""
    origins = []
    for item in value.split(','):
        item = item.strip().rstrip('/')
        if not item:
            continue
        if '*' in item:
            raise ValueError(f'wildcard origin refused: {item!r}')
        parts = urlsplit(item)
        if parts.scheme not in ('http', 'https') or not parts.hostname:
            raise ValueError(f'origin must be http(s)://host[:port]: {item!r}')
        if parts.path or parts.query or parts.fragment or parts.username:
            raise ValueError(f'origin must not carry a path or credentials: {item!r}')
        host = f'[{parts.hostname}]' if ':' in parts.hostname else parts.hostname
        if parts.scheme == 'http' and host not in LOOPBACK:
            raise ValueError(f'origin must use https unless loopback: {item!r}')
        if item not in origins:
            origins.append(item)
    if not origins:
        raise ValueError('WEB_ORIGIN needs at least one origin')
    return origins


def client_document(origins):
    origin = origins[0]
    return {
        'clientId': CLIENT_ID, 'name': 'SupportOps Console', 'enabled': True, 'protocol': 'openid-connect',
        'publicClient': True, 'standardFlowEnabled': True, 'directAccessGrantsEnabled': False,
        'implicitFlowEnabled': False, 'serviceAccountsEnabled': False, 'fullScopeAllowed': True,
        'rootUrl': origin, 'redirectUris': [o + '/' for o in origins], 'webOrigins': list(origins),
        'attributes': {'pkce.code.challenge.method': 'S256', 'post.logout.redirect.uris': '##'.join(o + '/' for o in origins)},
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
        with urlopen(request, context=context, timeout=30) as response:
            self.token = json.load(response)['access_token']

    def call(self, method, path, document=None):
        data = None if document is None else json.dumps(document).encode()
        request = Request(f'{self.base}/admin/realms/{REALM}{path}', data=data, method=method,
                          headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'})
        with urlopen(request, context=self.context, timeout=15) as response:
            raw = response.read()
        return json.loads(raw) if raw else None


def apply_client(admin, origins):
    wanted = client_document(origins)
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
    origins = parse_origins(os.environ['WEB_ORIGIN'])
    ca_file = os.environ.get('IDP_CA_FILE')
    context = ssl.create_default_context(cafile=ca_file) if ca_file else ssl.create_default_context()
    credentials_file = os.environ.get('IDP_CREDENTIALS_FILE')
    password = (json.loads(Path(credentials_file).read_text())['keycloak_admin'] if credentials_file
                else os.environ['IDP_ADMIN_PASSWORD'])
    deadline = time.monotonic() + 300
    while True:
        try:
            admin = Admin(os.environ['IDP_URL'], password, context)
            break
        except OSError as error:  # URLError, HTTPError and read timeouts while Keycloak boots
            if time.monotonic() > deadline:
                print(f'Keycloak admin login failed: {error}', file=sys.stderr)
                return 1
            time.sleep(3)
    apply_client(admin, origins)
    print(f'Applied OIDC client {CLIENT_ID} for {", ".join(origins)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
