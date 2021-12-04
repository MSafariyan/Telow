# FROM python:3.9
# RUN pythom -m pip intall --upgrade pip
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/

FROM python:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]