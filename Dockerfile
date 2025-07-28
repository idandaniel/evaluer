FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --only=main --no-root

COPY . .

RUN poetry install --only-root

RUN useradd --create-home --shell /bin/bash evaluer
RUN chown -R evaluer:evaluer /app
USER evaluer

EXPOSE 8000

CMD ["uvicorn", "evaluer.app:app", "--host", "0.0.0.0", "--port", "8000"]
