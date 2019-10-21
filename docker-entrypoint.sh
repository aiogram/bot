#!/usr/bin/env bash

set -e

PYTHON="python -O"
APP="${PYTHON} -m app"

# ${PYTHON} before_start.py

if [[ ! -z "${RUN_MIGRATIONS}" ]]; then
  alembic upgrade head
fi

case "$1" in
run-webhook)
  ${APP} webhook
  ;;
run-polling)
  ${APP} polling
  ;;
*)
  ${@}
esac
