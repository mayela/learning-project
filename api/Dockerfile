FROM python:3.12-alpine3.19

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./main.py main.py

COPY ./todos.json todos.json

ENTRYPOINT [ "fastapi", "dev","--host", "0.0.0.0", "main.py" ]
