FROM python:3.12.5-slim

LABEL authors="data-tamer2310"

WORKDIR /goit-pycore-hw-08

COPY . .

RUN pip install poetry && poetry install

CMD ["poetry", "run", "python", "project/main.py"]