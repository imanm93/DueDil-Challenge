FROM python:3.6.7

ADD . /api

WORKDIR /api

RUN pip3 install -r requirements.txt

CMD ["python3", "run.py"]
