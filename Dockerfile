FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app/

# Install system dependencies required for many Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    # Add other specific libraries here if needed (e.g., libpq-dev for Postgres, libjpeg-dev for Pillow)
    && rm -rf /var/lib/apt/lists/*

RUN ls -la requirements.txt # <-- Add this line to verify file presence
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit","run","app.py"]