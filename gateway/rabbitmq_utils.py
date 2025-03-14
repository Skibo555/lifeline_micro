import json
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def publish_event(event_name: str, message: dict):
    """Publish an event to RabbitMQ using a topic exchange."""
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # Declare an exchange (topic-based)
        exchange = await channel.declare_exchange("events_exchange", aio_pika.ExchangeType.TOPIC)

        body = json.dumps(message).encode()

        # Publish message to RabbitMQ
        await exchange.publish(
            aio_pika.Message(body=body),
            routing_key=event_name
        )

        print(f" [x] Sent '{event_name}': {message}")

