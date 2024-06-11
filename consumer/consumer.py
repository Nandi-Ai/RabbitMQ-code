import pika
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        print('Connected to RabbitMQ successfully.')

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("Interrupted, closing connection...")
        connection.close()

    except Exception as e:
        print(f"Error: {str(e)}")
        connection.close()

if __name__ == '__main__':
    main()
