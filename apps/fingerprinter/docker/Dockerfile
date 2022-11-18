FROM python:3.8-bullseye as builder

WORKDIR /app

ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache/poetry
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV PYTHONUNBUFFERED=1

RUN curl -sSLo install-poetry.sh https://install.python-poetry.org && \
  POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 install-poetry.sh && \
  rm install-poetry.sh

COPY poetry.lock poetry.toml pyproject.toml ./

RUN mkdir -p ${POETRY_CACHE_DIR}
RUN ${POETRY_HOME}/bin/poetry config --local virtualenvs.in-project true
RUN ${POETRY_HOME}/bin/poetry config --local virtualenvs.create true

# BUILDKIT cache
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
  ${POETRY_HOME}/bin/poetry install --no-interaction --no-ansi --no-root

FROM python:3.8-slim

WORKDIR /app
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=builder /app /app
COPY . .

ENTRYPOINT [ "/app/.venv/bin/python3", "-m" ]
CMD ["app.main"]
