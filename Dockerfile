FROM python:3.7-slim-buster as production
LABEL maintainer="Alex Root Junior <jroot.junior@gmail.com>" \
      description="Telegram Bot"

EXPOSE 80
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint
COPY Pipfile* /app/
RUN pip install pipenv && \
    pipenv install --system --deploy && \
    rm Pipfile* && \
    chmod +x /usr/bin/docker-entrypoint
ADD src /app/
RUN pybabel compile -d locales -D bot && find . -name "*.po*" -type f -delete

ENTRYPOINT ["docker-entrypoint"]
CMD ["run-webhook"]
