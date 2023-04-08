import pika
print('Started Consumer 1')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.21.0.1'))
channel = connection.channel()

channel.queue_declare(queue='health_check_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='health_check_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
