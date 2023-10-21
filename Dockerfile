FROM python:3

WORKDIR /code

COPY ./pyproject.toml .

RUN poetry install

COPY . .

CMD ["python", "manage.py", "runserver"]