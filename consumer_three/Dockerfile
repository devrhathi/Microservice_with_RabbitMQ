FROM python:3.10-slim-buster
RUN mkdir /consumer_three
WORKDIR /consumer_three
COPY . /consumer_three
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumer_three.py"]