# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install poetry


WORKDIR /home/app/backend
COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install
RUN poetry add debugpy
COPY . .