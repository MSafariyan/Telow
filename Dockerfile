FROM python:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]