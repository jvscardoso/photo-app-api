FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--debug", "run", "--host=0.0.0.0"]
