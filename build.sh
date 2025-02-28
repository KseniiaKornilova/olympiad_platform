#!/usr/bin/env bash
set -o errexit  

cd /opt/render/project/src
poetry install --only main
python manage.py migrate  
python manage.py collectstatic --no-input 