FROM python:3.10-slim-bullseye as production
LABEL maintainer="Alex Root Junior <jroot.junior@gmail.com>" \
      description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

EXPOSE 80
WORKDIR /app

# Install Poetry
RUN set +x \
 && apt update \
 && apt upgrade -y \
 && apt install -y curl gcc build-essential \
 && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -\
 && cd /usr/local/bin \
 && ln -s /opt/poetry/bin/poetry \
 && poetry config virtualenvs.create false \
 && rm -rf /var/lib/apt/lists/*

# Add code & install dependencies
ADD . /app/
RUN chmod +x scripts/* \
 && poetry install -n --only main \
 && pybabel compile -d locales -D bot

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run-webhook"]
