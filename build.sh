#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

export FLASK_APP=paperlight.py

flask db upgrade