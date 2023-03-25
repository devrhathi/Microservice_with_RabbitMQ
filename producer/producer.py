from flask import Flask, request
import pika

app = Flask(__name__)

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchanges and queues
channel.exchange_declare(exchange='health_check_exchange', exchange_type='direct')
channel.exchange_declare(exchange='database_exchange', exchange_type='direct')

channel.queue_declare(queue='health_check_queue', durable=True)
channel.queue_bind(exchange='health_check_exchange', queue='health_check_queue', routing_key='health_check_key')

channel.queue_declare(queue='insert_record_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='insert_record_queue', routing_key='insert_record_key')

channel.queue_declare(queue='read_database_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='read_database_queue', routing_key='read_database_key')

channel.queue_declare(queue='delete_record_queue', durable=True)
channel.queue_bind(exchange='database_exchange', queue='delete_record_queue', routing_key='delete_record_key')

# HTTP Server for health check
@app.route('/health_check', methods=['GET'])
def health_check():
    message = request.args.get('message')
    channel.basic_publish(exchange='health_check_exchange', routing_key='health_check_key', body=message)
    return 'Message published to health check queue'

# HTTP Server for inserting record
@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.get_json()
    name = data.get('name')
    srn = data.get('srn')
    section = data.get('section')
    message = f"{name},{srn},{section}"
    channel.basic_publish(exchange='database_exchange', routing_key='insert_record_key', body=message)
    return 'Record inserted'

# HTTP Server for reading all records
@app.route('/read_database', methods=['GET'])
def read_database():
    channel.basic_publish(exchange='database_exchange', routing_key='read_database_key', body='')
    return 'All records retrieved'

# HTTP Server for deleting record based on SRN
@app.route('/delete_record', methods=['GET'])
def delete_record():
    srn = request.args.get('srn')
    channel.basic_publish(exchange='database_exchange', routing_key='delete_record_key', body=srn)
    return f"Record with SRN {srn} deleted"

if __name__ == '__main__':
    print("Producer Started")
    app.run(host='0.0.0.0', port=5000, debug=True)
