FROM python:3.11-alpine3.19

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="/etc/poetry" \
    POETRY_CACHE_DIR="/tmp/poetry_cache" \
    POETRY_VERSION=1.7.0

WORKDIR /usr/src/app

COPY . .

RUN apk update 
RUN apk add --no-cache --virtual .dev gcc musl-dev libffi-dev
RUN apk add --no-cache cargo rust


RUN cargo init \
    && pip install maturin \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION" 
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi -vvv 
RUN pip uninstall -y poetry \
    && rm -rf /root/.cache \
    && rm -rf $POETRY_CACHE_DIR \
    && adduser -D appuser \
    && chown -R appuser:appuser .

USER appuser

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
