FROM quay.io/keycloak/keycloak:26.8.1
COPY --chown=keycloak:keycloak realm-template.json /opt/keycloak/realm-template.json
COPY --chown=keycloak:keycloak start-keycloak.sh /opt/keycloak/start-keycloak.sh
RUN chmod 0755 /opt/keycloak/start-keycloak.sh
# Without this, every cold start rebuilds Keycloak for minutes on a shared CPU.
# The public demo needs sign-in only. The Admin Console and the Admin REST API are switched off in the image, so
# they are not reachable from the internet. To run ops/stack/idp_clients.py again, build once without this flag.
RUN /opt/keycloak/bin/kc.sh build --db=postgres --health-enabled=true --features-disabled=admin,admin-api
ENTRYPOINT ["/opt/keycloak/start-keycloak.sh"]
