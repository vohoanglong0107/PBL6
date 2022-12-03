#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

FLASK_APP=app.manage flask db upgrade

exec gunicorn app.wsgi:app "$@"
