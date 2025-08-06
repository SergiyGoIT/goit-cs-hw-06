# Dockerfile
FROM python:3.12-slim

# Встановлення залежностей
WORKDIR /app
COPY . /app

RUN pip install pymongo

EXPOSE 3000
EXPOSE 5000

CMD ["python", "main.py"]
