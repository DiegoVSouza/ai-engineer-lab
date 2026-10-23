"""Generate stable, volume-backed credentials and a local HTTPS identity server."""

from datetime import datetime, timedelta, timezone
import ipaddress
import json
import os
from pathlib import Path
import secrets

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

ROOT = Path('/secrets')
for name in ('db', 'keycloak', 'p05', 'p04', 'grafana', 'credentials'):
    (ROOT / name).mkdir(parents=True, exist_ok=True)


def write(path, value, private=True):
    path.write_text(value, encoding='utf-8')
    path.chmod(0o600 if private and path.parent.name == 'credentials' else 0o444)


credentials_file = ROOT / 'credentials/credentials.json'
if credentials_file.exists():
    credentials = json.loads(credentials_file.read_text())
else:
    credentials = {key: secrets.token_hex(24) for key in (
        'db_admin', 'db_p04', 'db_p05', 'db_keycloak', 'keycloak_admin',
        'client_secret', 'agent_a', 'agent_b', 'approver_a', 'grafana',
        'jwt_secret', 'mcp_secret',
    )}
    write(credentials_file, json.dumps(credentials, indent=2) + '\n')

issuer_base = os.environ.get('LAB_IDP_URL', 'https://localhost:38443').rstrip('/')
issuer = issuer_base + '/realms/supportops'
ca_file = ROOT / 'credentials/ca.crt'
ca_key_file = ROOT / 'credentials/ca.key'
now = datetime.now(timezone.utc)
if ca_file.exists():
    ca_cert = x509.load_pem_x509_certificate(ca_file.read_bytes())
    ca_key = serialization.load_pem_private_key(ca_key_file.read_bytes(), password=None)
else:
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    ca_cert = None
try:
    if ca_cert is not None:
        ca_cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier)
except x509.ExtensionNotFound:
    ca_cert = None
if ca_cert is None:
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'SupportOps local CA')])
    ca_cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(subject)
               .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
               .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=3650))
               .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
               .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
               .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
               .add_extension(x509.KeyUsage(True, False, False, False, False, True, True, False, False), critical=True)
               .sign(ca_key, hashes.SHA256()))
    write(ca_key_file, ca_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                           serialization.NoEncryption()).decode())
    write(ca_file, ca_cert.public_bytes(serialization.Encoding.PEM).decode(), private=False)

server_cert = ROOT / 'keycloak/tls.crt'
renew = not server_cert.exists()
if not renew:
    existing_certificate = x509.load_pem_x509_certificate(server_cert.read_bytes())
    renew = existing_certificate.not_valid_after_utc < now+timedelta(days=30)
    try:
        existing_certificate.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier)
    except x509.ExtensionNotFound:
        renew = True
if renew:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'keycloak')])
    certificate = (x509.CertificateBuilder().subject_name(subject).issuer_name(ca_cert.subject)
                   .public_key(key.public_key()).serial_number(x509.random_serial_number())
                   .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=365))
                   .add_extension(x509.SubjectAlternativeName([
                       x509.DNSName('keycloak'), x509.DNSName('localhost'),
                       x509.IPAddress(ipaddress.ip_address('127.0.0.1')),
                   ]), critical=False)
                   .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
                   .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
                   .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
                   .add_extension(x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
                   .sign(ca_key, hashes.SHA256()))
    write(ROOT / 'keycloak/tls.key', key.private_bytes(serialization.Encoding.PEM,
          serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode())
    write(server_cert, certificate.public_bytes(serialization.Encoding.PEM).decode())
write(ROOT / 'p05/ca.crt', ca_file.read_text(), private=False)

write(ROOT / 'db/admin-password', credentials['db_admin'])
statements = []
for role in ('p04', 'p05', 'keycloak'):
    password = credentials['db_' + role]
    statements.extend([f"CREATE USER {role} WITH PASSWORD '{password}';", f'CREATE DATABASE {role} OWNER {role};'])
statements.extend(['\\connect p05', 'CREATE EXTENSION IF NOT EXISTS vector;'])
write(ROOT / 'db/01-databases.sql', '\n'.join(statements) + '\n')

keycloak_env = {
    'KC_DB': 'postgres', 'KC_DB_URL': 'jdbc:postgresql://postgres:5432/keycloak',
    'KC_DB_USERNAME': 'keycloak', 'KC_DB_PASSWORD': credentials['db_keycloak'],
    'KC_BOOTSTRAP_ADMIN_USERNAME': 'lab-admin', 'KC_BOOTSTRAP_ADMIN_PASSWORD': credentials['keycloak_admin'],
}
write(ROOT / 'keycloak/runtime.env', '\n'.join(f'export {key}={value}' for key,value in keycloak_env.items())+'\n')

scopes = ['ticket:read', 'ticket:write', 'task:read', 'task:write', 'triage:run',
          'billing:read', 'crm:read', 'refund:request', 'feedback:write', 'approval:decide']
mappers = [
    {'name': 'mcp-audience', 'protocol': 'openid-connect', 'protocolMapper': 'oidc-audience-mapper',
     'config': {'included.custom.audience': 'http://mcp:8000/mcp', 'access.token.claim': 'true',
                'introspection.token.claim': 'true'}},
    {'name': 'tenant', 'protocol': 'openid-connect', 'protocolMapper': 'oidc-usermodel-attribute-mapper',
     'config': {'user.attribute': 'tenant_id', 'claim.name': 'tenant_id', 'jsonType.label': 'String',
                'access.token.claim': 'true', 'introspection.token.claim': 'true'}},
    {'name': 'roles', 'protocol': 'openid-connect', 'protocolMapper': 'oidc-usermodel-realm-role-mapper',
     'config': {'claim.name': 'roles', 'multivalued': 'true', 'user.realmRole': 'true',
                'access.token.claim': 'true', 'introspection.token.claim': 'true'}},
    {'name': 'audience', 'protocol': 'openid-connect', 'protocolMapper': 'oidc-audience-mapper',
     'config': {'included.client.audience': 'supportops-api', 'access.token.claim': 'true',
                'introspection.token.claim': 'true'}},
]
users = []
for username, tenant, role, password_key in (
    ('agent-a','tenant-a','agent','agent_a'), ('agent-b','tenant-b','agent','agent_b'),
    ('approver-a','tenant-a','approver','approver_a'),
):
    users.append({'username':username, 'enabled':True, 'emailVerified':True,
                  'email':username+'@example.test', 'firstName':'Lab', 'lastName':role,
                  'requiredActions':[], 'attributes':{'tenant_id':[tenant]}, 'realmRoles':[role],
                  'credentials':[{'type':'password','value':credentials[password_key],'temporary':False}]})
realm = {
    'realm':'supportops', 'enabled':True, 'sslRequired':'all', 'accessTokenLifespan':300,
    'roles':{'realm':[{'name':'agent'},{'name':'approver'}]},
    'clientScopes':[{'name':scope,'protocol':'openid-connect',
                     'attributes':{'include.in.token.scope':'true'}} for scope in scopes],
    'clients':[{'clientId':'supportops-api','enabled':True,'protocol':'openid-connect',
                'publicClient':False,'secret':credentials['client_secret'],
                'standardFlowEnabled':True,'directAccessGrantsEnabled':True,'fullScopeAllowed':True,
                'redirectUris':['http://localhost:'+os.environ.get('LAB_API_PORT','48000')+'/docs/oauth2-redirect'],
                'optionalClientScopes':scopes,'protocolMappers':mappers}],
    'users':users,
}
write(ROOT / 'keycloak/supportops-realm.json', json.dumps(realm,indent=2)+'\n')

runtime = {
    'JWT_SECRET':credentials['jwt_secret'], 'MCP_SIGNING_SECRET':credentials['mcp_secret'],
    'P05_POSTGRES_DSN':f"postgresql://p05:{credentials['db_p05']}@postgres:5432/p05",
    'SSL_CERT_FILE':'/run/lab/ca.crt', 'API_AUTH_MODE':'oidc',
}
for prefix in ('API_OIDC','MCP_OIDC'):
    runtime.update({prefix+'_INTROSPECTION_URL':'https://keycloak:8443/realms/supportops/protocol/openid-connect/token/introspect',
                    prefix+'_CLIENT_ID':'supportops-api', prefix+'_CLIENT_SECRET':credentials['client_secret'],
                    prefix+'_ISSUER':issuer, prefix+'_AUDIENCE':'supportops-api'})
runtime['MCP_OIDC_AUDIENCE'] = 'http://mcp:8000/mcp'
write(ROOT / 'p05/runtime.json', json.dumps(runtime)+'\n')
write(ROOT / 'p04/runtime.json', json.dumps({'P04_DATABASE_URL':f"postgresql://p04:{credentials['db_p04']}@postgres:5432/p04"})+'\n')
write(ROOT / 'grafana/admin-password', credentials['grafana'])
print('Generated stable service credentials, database initialization, tenant realm and HTTPS certificate; secret values omitted.')
