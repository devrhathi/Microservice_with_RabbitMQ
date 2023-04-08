FROM python:3.10-slim-buster
RUN mkdir /consumer_two
WORKDIR /consumer_two
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer_two.py .
CMD [ "python", "./consumer_two.py" ]