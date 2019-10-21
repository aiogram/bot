#!/usr/bin/env bash

set -e

PYTHON="python -O"
APP="${PYTHON} -m app"

# ${PYTHON} before_start.py

case "$1" in
run-webhook)
  ${APP} webhook
  ;;
run-polling)
  ${APP} polling
  ;;
migrate)
  alembic upgrade head
  ;;
*)
  ${@}
esac
