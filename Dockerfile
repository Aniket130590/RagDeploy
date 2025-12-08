# Use a more complete base image that often resolves these issues implicitly, or
# stick with slim and explicitly install build tools:

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app/

# Install essential build tools and system dependencies required by many Python packages
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","app.py"]