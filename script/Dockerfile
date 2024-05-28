FROM python:3.9-slim

RUN pip install --no-cache-dir gunicorn
COPY wsgi.py /app/

WORKDIR /app

# 2 workers and port 8081
CMD ["gunicorn", "-b", "0.0.0.0:8081", "--workers", "2", "wsgi:application"]
