FROM python:3.8

WORKDIR /bprev

COPY . /bprev

RUN pip install -r requirements.txt

CMD ["python", "src/server.py"]