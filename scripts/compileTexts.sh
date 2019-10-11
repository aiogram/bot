#!/usr/bin/env bash

set -e
set -x

cd src/
pybabel compile -d locales -D bot
