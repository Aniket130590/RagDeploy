# Stage 1: Builder Stage - Handles all installations and heavy lifting
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

# Install build essentials for packages that need compilation
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use no-cache-dir to save disk space during installation
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final (Runtime) Stage - A clean environment for execution
FROM python:3.10-slim-bullseye AS runtime

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy the rest of your application code
COPY . /app/

EXPOSE 8501

CMD ["streamlit","run","app.py"]
