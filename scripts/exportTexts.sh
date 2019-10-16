#!/usr/bin/env bash

DOMAIN=bot
LOCALES_DIR=locales
PROJECT=aiogram_bot
VERSION=0.1

set -e
set -x

cd src/
pybabel extract . \
    -o ${LOCALES_DIR}/${DOMAIN}.pot \
    --project=${PROJECT} \
    --version=${VERSION} \
    --copyright-holder=Illemius \
    -k __:1,2 \
    --sort-by-file -w 99
pybabel update \
    -d ${LOCALES_DIR} \
    -D ${DOMAIN} \
    --update-header-comment \
    -i ${LOCALES_DIR}/${DOMAIN}.pot
