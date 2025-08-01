#!/bin/sh
set -e

python3 /app/supply.py &

exec nginx -g "daemon off;"