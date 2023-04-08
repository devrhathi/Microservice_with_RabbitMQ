FROM python:3.10-slim-buster
RUN mkdir /consumer_three
WORKDIR /consumer_three
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer_three.py .
CMD [ "python", "./consumer_three.py" ]