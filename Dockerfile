FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_DEBUG 1

ENV POSTGRES_USER xh4vm
ENV POSTGRES_PASSWORD xh4vm
ENV POSTGRES_DB justbegin

RUN apt-get update && apt-get install -y python-pip python-dev build-essential redis postgresql postgresql-client gcc python3-dev musl-dev
RUN pip install --upgrade pip

WORKDIR /justbegin 

COPY app app
COPY tests tests
COPY requirements.txt justbegin.py celery_worker.py config.py pytest.ini app_start.sh ./

RUN chmod +x app_start.sh

ENV FLASK_APP justbegin.py

RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "./app_start.sh" ]