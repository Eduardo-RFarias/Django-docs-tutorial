# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Turns off debug
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Install PipEnv
RUN pip install pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# collect static files
RUN python manage.py collectstatic --noinput

# Creating superuser
RUN python manage.py migrate \
    && python manage.py shell < scripts/create_superuser.py

# run gunicorn
CMD gunicorn admin.wsgi:application --bind 0.0.0.0:$PORT
