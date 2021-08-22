FROM python:3.9-slim-buster as production
LABEL maintainer="Alex Root Junior <jroot.junior@gmail.com>" \
      description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

EXPOSE 80
WORKDIR /app

# Install Poetry
RUN set +x \
 && apt update \
 && apt install -y curl \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
 && cd /usr/local/bin \
 && ln -s /opt/poetry/bin/poetry \
 && poetry config virtualenvs.create false \
 && rm -rf /var/lib/apt/lists/*

# Add code & install dependencies
ADD . /app/
RUN chmod +x scripts/* \
 && poetry install -n --no-dev \
 && pybabel compile -d locales -D bot

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run-webhook"]
