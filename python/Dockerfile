FROM python:3.7-slim-buster

COPY . /app
# WORKDIR /docker

RUN pip install -r app/requirements.txt

CMD ["python", "-u", "app/main.py"]