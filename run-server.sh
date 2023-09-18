#!/usr/bin/env bash
set -euo pipefail

echo Starting Server thru Gunicorn

cd app/
poetry shell
python manage.py migrate

gunicorn --bind 0.0.0.0:8000 --reload backend.wsgi
