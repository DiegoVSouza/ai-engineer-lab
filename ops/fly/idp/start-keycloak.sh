#!/bin/bash
set -euo pipefail

realm_dir=/opt/keycloak/data/import
mkdir -p "$realm_dir"
sed \
  -e "s|__CLIENT_SECRET__|${SUPPORTOPS_CLIENT_SECRET}|g" \
  -e "s|__AGENT_A_PASSWORD__|${SUPPORTOPS_AGENT_A_PASSWORD}|g" \
  -e "s|__AGENT_B_PASSWORD__|${SUPPORTOPS_AGENT_B_PASSWORD}|g" \
  -e "s|__APPROVER_PASSWORD__|${SUPPORTOPS_APPROVER_PASSWORD}|g" \
  /opt/keycloak/realm-template.json > "$realm_dir/supportops-realm.json"

exec /opt/keycloak/bin/kc.sh start --import-realm
