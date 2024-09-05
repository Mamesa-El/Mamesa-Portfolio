ARG APP_DIR=/APP_DIR

FROM python:3.10-slim as build
ARG APP_DIR

RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/POETRY_HOME
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies ${APP_DIR}/venv
RUN . /${APP_DIR}/venv/bin/activate && poetry install --only main

FROM python:3.10-slim as deploy
ARG APP_DIR

WORKDIR ${APP_DIR}
COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv
ENV PATH=${APP_DIR}/venv/bin:${PATH}

ENV REDIS_HOST="redis"

COPY . .

# HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]

# Health check to poll the /health endpoint
# HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1


# ARG APP_DIR=/APP_DIR

# FROM python:3.10-slim as build
# ARG APP_DIR

# RUN apt-get update \
#     && apt-get install -y \
#          curl \
#          build-essential \
#          libffi-dev \
#     && rm -rf /var/lib/apt/lists/*

# ENV POETRY_VERSION=1.6.1
# ENV POETRY_HOME=/opt/POETRY_HOME
# ENV PATH=${POETRY_HOME}/bin:${PATH}
# RUN curl -sSL https://install.python-poetry.org | python3 -

# # Adjust these COPY commands to include the directory name 'mlapi'
# COPY mlapi/pyproject.toml mlapi/poetry.lock ./
# RUN python -m venv --copies ${APP_DIR}/venv
# RUN . /${APP_DIR}/venv/bin/activate && poetry install --only main

# FROM python:3.10-slim as deploy
# ARG APP_DIR

# WORKDIR ${APP_DIR}
# COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv
# ENV PATH=${APP_DIR}/venv/bin:${PATH}

# ENV REDIS_HOST="redis-service"

# # Adjust these COPY commands to include the directory names
# COPY mlapi/src ./src
# COPY distilbert-base-uncased-finetuned-sst2 ./distilbert-base-uncased-finetuned-sst2

# # Optional health checks
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]

