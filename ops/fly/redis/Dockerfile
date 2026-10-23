FROM redis@sha256:becdda6c7f4b3fb42e42fd7f120bbf5c54c4caaaf16f26da24e4563d2c1f0576
COPY start-redis.sh /usr/local/bin/start-redis
RUN chmod 0755 /usr/local/bin/start-redis
ENTRYPOINT ["/usr/local/bin/start-redis"]
