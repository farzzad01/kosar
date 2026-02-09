#!/usr/bin/env bash
set -o errexit

pip install --break-system-packages -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate --no-input
