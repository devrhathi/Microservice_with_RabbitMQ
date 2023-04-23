#Importing required modules
import pika
import pymongo

#Establishing connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1'))
channel = connection.channel()

#Declaring queue for receiving messages
channel.queue_declare(queue='delete_record_queue', durable=True)

#Establishing connection with MongoDB server
client = pymongo.MongoClient("mongodb://database:27017/", username='root', password='ccproject')

db = client["mydatabase"]
col = db["students"]


#Callback function for receiving messages and deleting records from MongoDB
def callback(ch, method, properties, body):
    srn = body.decode().strip()
    myquery = {"srn": srn}
    x = col.delete_many(myquery)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
#Consume messages from RabbitMQ queue
channel.basic_consume(queue='delete_record_queue', on_message_callback=callback)

#Start consuming messages
print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
channel.start_consuming()
