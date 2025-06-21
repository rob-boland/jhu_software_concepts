FROM python:3.10

RUN mkdir /app

WORKDIR /app

ADD run.py .

RUN pip install requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]