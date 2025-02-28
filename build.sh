#!/usr/bin/env bash
set -o errexit  

poetry install --only main
python ./olympiad_platform/manage.py migrate  
python ./olympiad_platform/manage.py collectstatic --no-input 