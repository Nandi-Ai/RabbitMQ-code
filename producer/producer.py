import pika
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")


connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

channel.queue_declare(queue='hello')

# Send a message
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!2')
print(" [x] Sent 'Hello World!2'")

# Close the connection
connection.close()
