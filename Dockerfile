FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app/

#RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN pip install -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit","run","app.py"]

