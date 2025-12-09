FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app/

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
#RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","app.py"]