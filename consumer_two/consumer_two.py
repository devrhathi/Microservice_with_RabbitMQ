import pika
import pymongo

# create a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.21.0.1'))
channel = connection.channel()

# declare a queue named 'insert_record_queue'
channel.queue_declare(queue='insert_record_queue', durable=True)

# create a client for connecting to MongoDB database
client = pymongo.MongoClient("mongodb://database:27017/", username='root', password='ccproject')
db = client["mydatabase"]
col = db["students"]

# define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    # decode the message and split it into separate fields
    data = body.decode().split(',')
    name = data[0].strip()
    srn = data[1].strip()
    section = data[2].strip()
    
    # create a dictionary to represent the new record
    mydict = {"name": name, "srn": srn, "section": section}
    
    # insert the record into the MongoDB collection
    x = col.insert_one(mydict)
    
    # print the inserted record's ID for debugging purposes
    print(x.inserted_id,flush=True)
    
    # acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# register the callback function to consume messages from 'insert_record_queue'
channel.basic_consume(queue='insert_record_queue', on_message_callback=callback)

# start consuming messages from the queue
print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
channel.start_consuming()
