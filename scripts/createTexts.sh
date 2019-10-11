#!/usr/bin/env bash

set -e
set -x

pybabel init -i src/locales/bot.pot -d src/locales -D bot -l $1
