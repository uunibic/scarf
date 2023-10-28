# base image
FROM python:3.9-alpine

# setup environment variable
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /app

# where code lives
WORKDIR /app

# copy the current directory contents into the container at /w
RUN apk add py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango
COPY ./ascart ./ascart
COPY ./codereview ./codereview
COPY ./manage.py .
COPY ./requirements.txt .
COPY ./.env .


# install needed packages
RUN apk update
RUN apk add --no-cache libffi-dev build-base pango-dev ttf-freefont fontconfig
RUN fc-cache -f
RUN pip install --no-cache-dir -r requirements.txt

# port where django app runs
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000

# start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]