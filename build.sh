#!/usr/bin/env bash
# Render build script (also works locally to test deployment build).
set -o errexit
set -o pipefail

pip install --upgrade pip
pip install pipenv
pipenv install --deploy --system
python manage.py collectstatic --noinput
