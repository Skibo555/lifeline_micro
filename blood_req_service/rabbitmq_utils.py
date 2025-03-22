import json
from datetime import datetime
import aio_pika
import asyncio

from database import get_db
from models.request_model import Request
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import func

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converts datetime to a string
    raise TypeError(f"Type {type(obj)} is not serializable")

RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"
SERVICE_QUEUE_NAME = "request_service"


async def process_message(message: aio_pika.IncomingMessage):
    """
    Processes incoming RabbitMQ messages.
    """
    async with message.process():  
        try:
            body = message.body.decode()
            data = json.loads(body)
            event_name = message.routing_key 
         

            print(f"📩 [{SERVICE_QUEUE_NAME}] Received event: {event_name}, Data: {data}")

        except Exception as e:
            print(f"⚠️ Error processing message: {e}")
            await message.nack(requeue=False)  # Reject message permanently if error occurs


async def consume():
    """
    Consumer function to listen for RabbitMQ events.
    """
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)
            queue = await channel.declare_queue(SERVICE_QUEUE_NAME, durable=True)

            # await queue.bind(exchange, routing_key="request.created")
            await queue.bind(exchange, routing_key="#")

            await channel.set_qos(prefetch_count=1)
            await queue.consume(process_message)

            print(f" [*] Waiting for events on {SERVICE_QUEUE_NAME}...")
            await asyncio.Future()  # Keep running forever

        except Exception as e:
            print(f"⚠️ Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()



