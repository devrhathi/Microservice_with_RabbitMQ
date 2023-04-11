import pika
import pymongo

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.28.0.1'))
channel = connection.channel()

channel.queue_declare(queue='delete_record_queue', durable=True)

client = pymongo.MongoClient("mongodb://database:27017/", username='root', password='ccproject')

db = client["mydatabase"]
col = db["students"]

def callback(ch, method, properties, body):
    srn = body.decode().strip()
    myquery = {"srn": srn}
    x = col.delete_many(myquery)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='delete_record_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
channel.start_consuming()
