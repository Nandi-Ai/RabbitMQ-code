import pika
import time

class RabbitMQClient:
    def __init__(self, host='localhost', queue='my_queue'):
        self.host = host
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

##push message to queue
    def push_message(self, message, message_id=None):
        if message_id:
            message += f" (ID: {message_id})"

        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f" [x] Sent '{message}'")

##Retrieves the current depth (number of messages) of the queue.
    def get_queue_depth(self):
        queue = self.channel.queue_declare(queue=self.queue, passive=True)
        depth = queue.method.message_count
        print(f" [x] Queue depth is {depth}")
        return depth
    
##Deletes all messages from the queue.
    def delete_all_messages(self):
        # Get the initial queue depth
        initial_depth = self.get_queue_depth()
    
        # Delete messages until the queue is empty
        while initial_depth > 0:
            method_frame, _, _ = self.channel.basic_get(queue=self.queue, auto_ack=False)
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        
            # Decrement the initial_depth after each deletion
            initial_depth -= 1
        print(" [x] All messages deleted")

##Delete specific message -- not done !
    def delete_message_by_id(self, message_id):
        while True:
            method_frame, _, body = self.channel.basic_get(queue=self.queue, auto_ack=False)
            if method_frame:
                decoded_body = body.decode()
                if f"(ID: {message_id})" in decoded_body:
                    self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    print(f" [x] Message with ID '{message_id}' deleted")
                    break
            else:
                print(f" [x] Message with ID '{message_id}' not found in queue")
                break

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    client = RabbitMQClient()
    client.delete_all_messages()
    
    time.sleep(1)  # Wait for 1 second
    client.get_queue_depth()
    # Push some messages
    client.push_message("Message 1")
    client.push_message("Message 2", message_id=2)
    client.push_message("Message 3", message_id=3)
    client.push_message("Message 4")

    time.sleep(1)  # Wait for 1 second
    client.get_queue_depth()

    # Delete message with ID '2'
    client.delete_message_by_id(2)

    time.sleep(2)  # Wait for 1 second

    client.get_queue_depth()

    client.close_connection()