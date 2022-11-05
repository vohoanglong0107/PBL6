FROM python:3.8-bullseye as builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# BUILDKIT cache
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends git=1:2.30.2-1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY . /app/

ENV MLFLOW_TRACKING_URI=
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT [ "python" ]

CMD [ "reinforce.py" ]