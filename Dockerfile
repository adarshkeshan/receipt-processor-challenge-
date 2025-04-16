FROM python:3.9-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && chown -R nobody:nogroup /app/data
USER nobody

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
# ENV FLASK_DEBUG=0
ENV FLASK_DEBUG=1

ENV DATABASE_FOLDER=/app/data

CMD ["flask", "run"]
