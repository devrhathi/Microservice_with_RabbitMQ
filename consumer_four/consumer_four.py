import pika
import pymongo

print('Started Consumer 4')


connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.21.0.1'))
channel = connection.channel()

channel.queue_declare(queue='read_database_queue', durable=True)

client = pymongo.MongoClient("mongodb://mongodb:27017/", username='root', password='ccproject')

db = client["mydatabase"]
col = db["students"]

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    docs = col.find()
    for doc in docs:
        print(doc)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='read_database_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
