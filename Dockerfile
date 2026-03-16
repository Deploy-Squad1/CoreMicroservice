FROM python:3.13-slim AS build-stage

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies to compile psycopg 3
RUN apt update && apt install -y \
    libpq-dev \
    python3-dev \
    gcc 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim AS production-stage

COPY --from=build-stage /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=build-stage /usr/local/bin/ /usr/local/bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Needed for psycopg 3 to run
RUN apt update && apt install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000 

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
