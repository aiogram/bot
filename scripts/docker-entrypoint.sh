#!/usr/bin/env bash

set -e

PYTHON="python -O"
APP="exec ${PYTHON} -m app"

${PYTHON} -m app.utils.before_start

function migrate () {
  if [[ ! -z "${RUN_MIGRATIONS}" ]]; then
    alembic upgrade head
  fi
}

case "$1" in
  run-webhook)
    migrate
    ${APP} webhook
    ;;

  run-polling)
    migrate
    ${APP} polling
    ;;

  *)
    ${@}

esac
