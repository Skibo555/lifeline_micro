import pika
import json


RABBITMQ_HOST = "localhost"

def publish_hospital_created_event(user_id: str, hospital_id: str, hospital_name: str):
    """Publishes an event when a hospital is created"""
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue="hospital_created_queue", durable=True)

    # Message payload
    message = {
        "user_id": user_id,
        "hospital_id": hospital_id,
        "hospital_name": hospital_name
    }

    # Publish message
    channel.basic_publish(
        exchange="",
        routing_key="hospital_created_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Makes message persistent
        ),
    )

    print(f" [x] Sent hospital created event: {message}")

    connection.close()


