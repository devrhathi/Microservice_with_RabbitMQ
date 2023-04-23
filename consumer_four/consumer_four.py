
#  Importing necessary libraries
import pika
import pymongo

#Establishing connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1'))
channel = connection.channel()

#Declaring the queue to receive messages from
channel.queue_declare(queue='read_database_queue', durable=True)


#Establishing connection to MongoDB server
client = pymongo.MongoClient("mongodb://database:27017/", username='root', password='ccproject')

#Accessing the "mydatabase" database
db = client["mydatabase"]

# Accessing the "students" collection
col = db["students"]

#Callback function to be executed when a message is received
def callback(ch, method, properties, body):
    docs = col.find()
    for doc in docs:
        print(doc,flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
#Consuming messages from the queue and executing the callback function
channel.basic_consume(queue='read_database_queue', on_message_callback=callback)

#Starting to consume messages
print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
channel.start_consuming()
