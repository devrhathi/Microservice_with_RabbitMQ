# Importing required modules
from flask import Flask, request
import pika
import time

# Initializing Flask app
app = Flask(__name__)

# Establishing RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1', heartbeat=800))
channel = connection.channel()

# Declaring exchanges and queues
channel.exchange_declare(exchange='health_check_exchange', exchange_type='direct') # Creating a direct exchange for health checks
channel.exchange_declare(exchange='database_exchange', exchange_type='direct') # Creating a direct exchange for database operations

channel.queue_declare(queue='health_check_queue', durable=True) # Declaring a durable queue for health checks
channel.queue_bind(exchange='health_check_exchange', queue='health_check_queue', routing_key='health_check_key') # Binding the health check queue to the health check exchange with a specific routing key

channel.queue_declare(queue='insert_record_queue', durable=True) # Declaring a durable queue for inserting records
channel.queue_bind(exchange='database_exchange', queue='insert_record_queue', routing_key='insert_record_key') # Binding the insert record queue to the database exchange with a specific routing key

channel.queue_declare(queue='delete_record_queue', durable=True) # Declaring a durable queue for deleting records
channel.queue_bind(exchange='database_exchange', queue='delete_record_queue', routing_key='delete_record_key') # Binding the delete record queue to the database exchange with a specific routing key

channel.queue_declare(queue='read_database_queue', durable=True) # Declaring a durable queue for reading all records
channel.queue_bind(exchange='database_exchange', queue='read_database_queue', routing_key='read_database_key') # Binding the read database queue to the database exchange with a specific routing key

# HTTP Server for health check
@app.route('/health_check', methods=['GET']) # Defining an HTTP GET route for health check
def health_check():
    message = request.args.get('message') # Extracting the message parameter from the GET request
    if(message == None):
        return 'Please enter message as a parameter to the GET request'
    channel.basic_publish(exchange='health_check_exchange', routing_key='health_check_key', body=message) # Publishing the message to the health check exchange
    return f"The Message:{message.decode()} has been effectively delivered and stored in the health check queue"

# HTTP Server for inserting record
@app.route('/insert_record', methods=['POST']) # Defining an HTTP POST route for inserting records
def insert_record():
    data = request.get_json() # Extracting the JSON data from the POST request
    name = data.get('name') # Extracting the name field from the JSON data
    srn = data.get('srn') # Extracting the srn field from the JSON data
    section = data.get('section') # Extracting the section field from the JSON data
    message = f"{name},{srn},{section}" # Creating a comma-separated string from the extracted fields
    channel.basic_publish(exchange='database_exchange', routing_key='insert_record_key', body=message) # Publishing the message to the insert record queue
    return 'Record inserted'

# HTTP Server for deleting record based on SRN
@app.route('/delete_record', methods=['GET']) # Defining an HTTP GET route for deleting records
def delete_record():
    srn = request.args.get('srn') # Extracting the srn parameter from the GET request
    result = channel.basic_publish(exchange='database_exchange', routing_key='delete_record
