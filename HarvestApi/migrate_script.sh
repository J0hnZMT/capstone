#!/bin/bash

python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
gunicorn -b 0.0.0.0:8000 run:application