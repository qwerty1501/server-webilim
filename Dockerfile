# pull python base image
FROM python:3.9

# set working derictory
WORKDIR /app/

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . /app

CMD ['python', 'manage.py', 'runserver 0.0.0.0:8000']