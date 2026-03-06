# multi-stage build
# non-root user
# use alpine or slim base image

# stage 1 : builder

FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
# Reduce image size: using --no-cache-dir
RUN pip install --prefix=/app --no-cache-dir -r requirements.txt

# stage 2 : prod image

FROM python:3.12-slim as prod

WORKDIR /app

RUN useradd -m appuser

COPY --from=builder /app /usr/local

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]

