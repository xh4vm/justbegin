#!/bin/sh
flask db init
flask db migrate
flask db upgrade

/etc/init.d/redis-server restart 
celery -A celery_worker.celery worker &
exec gunicorn -b :5000 --access-logfile - --error-logfile - justbegin:app