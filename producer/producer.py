# Import necessary libraries
from flask import Flask, request
import pika
import time

# Initialize Flask application
app = Flask(__name__)

# Establish RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1', heartbeat=800))
channel = connection.channel()

# Declare exchanges and queues
channel.exchange_declare(exchange='health_check_exchange', exchange_type='direct')
channel.exchange_declare(exchange='database_exchange', exchange_type='direct')

channel.queue_declare(queue='health_check_queue', durable=True)
channel.queue_bind(exchange='health_check_exchange', queue='health_check_queue', routing_key='health_check_key')

channel.queue_declare(queue='insert_record_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='insert_record_queue', routing_key='insert_record_key')

channel.queue_declare(queue='delete_record_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='delete_record_queue', routing_key='delete_record_key')

channel.queue_declare(queue='read_database_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='read_database_queue', routing_key='read_database_key')

# HTTP Server for health check
@app.route('/health_check', methods=['GET'])
def health_check():
    message = request.args.get('message')
    # Return error message if message is not provided in GET request parameters
    if(message == None):
        return 'Please enter message as a parameter to the GET request'
    # Publish message to the health check queue
    channel.basic_publish(exchange='health_check_exchange', routing_key='health_check_key', body=message)
    return f"The Message:{message.decode()} has been effectively delivered and stored in the health check queue"

# HTTP Server for inserting record
@app.route('/insert_record', methods=['POST'])
def insert_record():
    # Extract data from POST request JSON
    data = request.get_json()
    name = data.get('name')
    srn = data.get('srn')
    section = data.get('section')
    # Combine extracted data to form message to be published to the insert record queue
    message = f"{name},{srn},{section}"
    # Publish message to the insert record queue
    channel.basic_publish(exchange='database_exchange', routing_key='insert_record_key', body=message)
    return 'Record inserted'

# HTTP Server for deleting record based on SRN
@app.route('/delete_record', methods=['GET'])
def delete_record():
    srn = request.args.get('srn')
    # Publish SRN as message to the delete record queue
    result = channel.basic_publish(exchange='database_exchange', routing_key='delete_record_key', body=srn)
    return f"Record with SRN {srn} deleted"

# HTTP Server for reading all records
@app.route('/read_database', methods=['GET'])
def read_database():
    # Publish empty message to read database queue
    channel.basic_publish(exchange='database_exchange', routing_key='read_database_key', body='')
    return 'All records retrieved'

# Main function
if __name__ == '__main__':
    # Start Flask application
    print("Producer Started")
    app.run(host='0.0.0.0', port=5000, debug=True)
