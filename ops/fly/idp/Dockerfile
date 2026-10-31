FROM quay.io/keycloak/keycloak:26.8.1
COPY --chown=keycloak:keycloak realm-template.json /opt/keycloak/realm-template.json
COPY --chown=keycloak:keycloak start-keycloak.sh /opt/keycloak/start-keycloak.sh
RUN chmod 0755 /opt/keycloak/start-keycloak.sh
# Without this, every cold start rebuilds Keycloak for minutes on a shared CPU.
RUN /opt/keycloak/bin/kc.sh build --db=postgres --health-enabled=true
ENTRYPOINT ["/opt/keycloak/start-keycloak.sh"]
