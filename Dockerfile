FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip python-dev build-essential redis postgresql postgresql-client gcc python3-dev musl-dev
RUN pip install --upgrade pip

WORKDIR /justbegin 

COPY app app
COPY tests tests
COPY requirements.txt justbegin.py celery_worker.py config.py pytest.ini app_start.sh ./

RUN chmod +x app_start.sh

ENV FLASK_APP justbegin.py

RUN pip3 install -r requirements.txt

RUN sed -e "s/from werkzeug import secure_filename, FileStorage/from werkzeug.utils import secure_filename\nfrom werkzeug.datastructures import  FileStorage/g" /usr/local/lib/python3.8/site-packages/flask_uploads.py > /usr/local/lib/python3.8/site-packages/flask_uploads.py_new
RUN mv /usr/local/lib/python3.8/site-packages/flask_uploads.py_new /usr/local/lib/python3.8/site-packages/flask_uploads.py

EXPOSE 5000
ENTRYPOINT [ "./app_start.sh" ]