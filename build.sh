#!/usr/bin/env bash
# build.sh
pip install -r requirements.txt
# Aplicar migraciones y recolectar archivos estáticos
python manage.py migrate
python manage.py collectstatic --noinput
