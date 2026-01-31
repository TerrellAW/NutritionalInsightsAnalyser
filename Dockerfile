FROM python:latest

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt

CMD ["python", "data_analysis.py"]
