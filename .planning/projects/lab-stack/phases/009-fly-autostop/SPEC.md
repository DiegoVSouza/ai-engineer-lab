# Specification

The owner asked for auto stop on the whole Fly stack ("deixa auto stop em tudo"), so idle compute costs nothing.

Fly Proxy only stops and wakes machines it routes to. Therefore:

- `db`, `redis`, `sns` and `jaeger` get a private Flycast address and a raw TCP service, and clients use `<app>.flycast` instead of `.internal`. They never get a public address.
- `idp` stops at idle.
- P04 and P05 workers move into the API machine. A worker receives no traffic, so it cannot be woken, and while running it would keep the database and Redis awake. Jobs are durable, so a stopped machine resumes them on the next wake.

The cost is a cold start of one to two minutes after idle, and the console may ask for sign-in again.
