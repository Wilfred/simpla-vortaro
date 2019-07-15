FROM python:2-buster

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install -r requirements_pinned.txt

RUN python manage.py collectstatic --noinput && python manage.py syncdb

EXPOSE 9001
CMD ["gunicorn", "wsgi", "--worker-tmp-dir=/dev/shm", "-b", "0.0.0.0:9001", "--log-file=-", "--workers=2"]
