from datetime import datetime
import uuid
import json
import aio_pika
import asyncio


RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converts datetime to a string
    elif isinstance(obj, uuid.UUID):
        return str(obj)  # Converts UUID to string
    raise TypeError(f"Type {type(obj)} is not serializable")


class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """Connects to RabbitMQ and initializes the exchange."""
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()
        await self.channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)

    async def publish_event(self, event_name: str, data: dict):
        """Publishes an event to the RabbitMQ exchange."""
        if not self.channel:
            await self.connect()

        message_body = json.dumps({"event": event_name, "data": data}, default=json_serializer)

        exchange = await self.channel.get_exchange(EXCHANGE_NAME)

        await exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=event_name
        )

        print(f"✅ Publishing: {event_name} to exchange: {EXCHANGE_NAME}")

# Global instance
rabbitmq_service = RabbitMQService()