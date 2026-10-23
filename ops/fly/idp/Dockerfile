FROM quay.io/keycloak/keycloak:26.8.1
COPY --chown=keycloak:keycloak realm-template.json /opt/keycloak/realm-template.json
COPY --chown=keycloak:keycloak start-keycloak.sh /opt/keycloak/start-keycloak.sh
RUN chmod 0755 /opt/keycloak/start-keycloak.sh
ENTRYPOINT ["/opt/keycloak/start-keycloak.sh"]
