#!/usr/bin/env bash

set -e

python -O -m app version
python -O before_start.py

if [[ "$1" == "run-webhook" ]]; then
  echo "start bot with webhook"
elif [[ "$1" == "run-polling" ]]; then
  python -m app polling
else
  exec "${@}"
fi
