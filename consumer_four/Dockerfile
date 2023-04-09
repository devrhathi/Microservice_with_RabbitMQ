FROM python:3.10-slim-buster
RUN mkdir /consumer_four
WORKDIR /consumer_four
COPY . /consumer_four
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumer_four.py"]