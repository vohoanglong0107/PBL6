FROM python:3.8-bullseye as builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# BUILDKIT cache
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY . /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT [ "python" ]

CMD [ "processing.py" ]