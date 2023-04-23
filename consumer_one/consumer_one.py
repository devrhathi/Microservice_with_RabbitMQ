import pika

# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.21.0.1'))
channel = connection.channel()

# Declare a queue named 'health_check_queue' with durable=True to ensure messages are not lost even if RabbitMQ server restarts
channel.queue_declare(queue='health_check_queue', durable=True)

# Define a callback function to handle messages received on 'health_check_queue'
def callback(ch, method, properties, body):
    # Print the received message to console
    print(" [x] Received %r" % body.decode(), flush=True)
    # Acknowledge receipt of the message to RabbitMQ server
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages on 'health_check_queue' using the callback function defined above
channel.basic_consume(queue='health_check_queue', on_message_callback=callback)

# Start consuming messages indefinitely until the script is interrupted
print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
channel.start_consuming()

