FROM python:3.8-bullseye as builder

WORKDIR /app

ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV PYTHONUNBUFFERED=1

RUN curl -sSLo install-poetry.sh https://install.python-poetry.org && \
  POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 install-poetry.sh && \
  rm install-poetry.sh

COPY poetry.lock poetry.toml pyproject.toml ./

RUN ${POETRY_HOME}/bin/poetry export -f requirements.txt --output requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip wheel --no-deps --wheel-dir /app/dist -r requirements.txt

FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir ./*.whl && rm -rf ./*.whl

RUN apt-get update && \
  apt-get install -y --no-install-recommends libsndfile1=1.0.31-2 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY . .

ENTRYPOINT [ "python3", "-m" ]
CMD ["app.main", "train"]
