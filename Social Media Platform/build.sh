#!/bin/bash
set -e
pip3 install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput
python3 manage.py migrate
