FROM pgvector/pgvector:0.8.7-pg16
COPY init-databases.sh /docker-entrypoint-initdb.d/10-init-databases.sh
RUN chmod 0755 /docker-entrypoint-initdb.d/10-init-databases.sh
