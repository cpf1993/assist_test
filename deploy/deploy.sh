#!/bin/bash

HOME=/home/admin

VENV_PATH=$HOME/py_venvs/py3

APP_NAME=assist_test
APP_PATH=$HOME/apps/$APP_NAME
APP_LOG_PATH=$HOME/logs/$APP_NAME

# switch pms virtual env
. $VENV_PATH/bin/activate
env |grep VIRTUAL_ENV |wc -l

# go to project dir
cd $APP_PATH

# install python libs
pip install -r requirement.txt --extra-index-url http://web:xxxx  --extra-index-url  http://web:xxxxxxx --trusted-host 127.0.0.1

# collect & compress static files
python manage.py collectstatic --settings=assist_test.settings.front --noinput
# python manage.py compress --settings=assist_test.settings.front

# restart all services of the app
supervisorctl -s "http://localhost:9001" -u user -p 123 restart assist_service_group:*
