FROM python:3.8.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app
RUN apt-get update 
RUN apt-get install libpq-dev gcc libcairo2 pango1.0-tests python3-dev python3-psycopg2 postgresql postgresql-contrib nginx -y
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app
RUN rm /etc/nginx/sites-enabled/*
COPY nginx.conf /etc/nginx/sites-enabled/
EXPOSE 80
