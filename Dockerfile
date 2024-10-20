FROM python:3.12-slim

LABEL authors="data-tamer2410"

WORKDIR /ds-console-bot-helper

COPY . .

RUN pip install poetry && poetry install

CMD ["poetry", "run", "python", "project/main.py"]
