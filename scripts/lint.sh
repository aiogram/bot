#!/usr/bin/env bash

set -e
set -x

isort --recursive src/
black src/
flake8 src/
