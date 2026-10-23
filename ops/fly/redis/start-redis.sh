#!/bin/sh
set -eu
exec redis-server --appendonly yes --appendfsync everysec --save 60 1000 --requirepass "$REDIS_PASSWORD"
