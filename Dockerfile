# Dockerfile contents (assuming you are using the slim image)
FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app/

# ADDED: Install build tools needed by many Python packages
RUN apt-get update && apt-get install -y build-essential \
    # Optional clean up line to keep image size small
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","app.py"]
