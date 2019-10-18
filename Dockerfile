FROM python:3.7-slim-buster as production
LABEL maintainer="jroot.junior@gmail.com" \
      description="Telegram Bot"

EXPOSE 80
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint
RUN chmod +x /usr/bin/docker-entrypoint
COPY Pipfile* /app/
RUN pip install pipenv && \
	pipenv install --system --deploy && \
	rm Pipfile*
ADD src /app/
RUN pybabel compile -d locales -D bot && find . -name "*.po*" -type f -delete

ENTRYPOINT ["docker-entrypoint"]
CMD ["run-webhook"]
