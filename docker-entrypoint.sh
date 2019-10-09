#!/usr/bin/env bash

set -e

PYTHON="python -O"
APP="${PYTHON} -m app"

${PYTHON} before_start.py

if [[ "$1" == "run-webhook" ]]; then
  ${APP} webhook
elif [[ "$1" == "run-polling" ]]; then
  ${APP} polling
else
  ${@}
fi
