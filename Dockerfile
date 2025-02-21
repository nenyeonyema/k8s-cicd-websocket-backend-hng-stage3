# Dockerfile
FROM python:3.9

WORKDIR /app

COPY helloworld.py test_helloworld.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "helloworld.py"]

