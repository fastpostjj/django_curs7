#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput
celery -A config.celery flower worker --beat --loglevel=info -D