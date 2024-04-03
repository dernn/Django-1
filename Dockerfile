FROM python:3.10.2-alpine

RUN mkdir code
WORKDIR code

# COPY same as ADD below
ADD . /code/
ADD .env.docker /code/.env

# EXPOSE

RUN pip install -r requirements.txt

CMD gunicorn project.wsgi:application -b 0.0.0.0:8000