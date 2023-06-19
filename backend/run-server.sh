#!/usr/bin/env bash
set -euo pipefail

echo Starting Server thru Gunicorn

poetry run python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 --reload backend.wsgi
