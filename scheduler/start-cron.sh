#!/bin/sh
set -e

echo "Starting scheduler container..."

printenv > /etc/environment

exec cron -f
