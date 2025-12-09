FROM python:3.9-slim-buster

WORKDIR /app

COPY RAGProject/requirements.txt/requirements.txt .  # Copies to /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8501

CMD ["streamlit","run","app.py"]

