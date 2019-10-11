FROM python:3.7-slim-buster as production
MAINTAINER Alex Root Junior

# Prepare workspace
EXPOSE 80
WORKDIR /app
COPY docker-entrypoint.sh /usr/bin/docker-entrypoint
RUN chmod +x /usr/bin/docker-entrypoint

# Install dependencies
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && \
	pipenv install --system --deploy && \
	rm Pipfile*

# Add source code
ADD src .
RUN pybabel compile -d locales -D bot && find . -name "*.po*" -type f -delete

# Execution
ENTRYPOINT ["docker-entrypoint"]
CMD ["run-polling"]
