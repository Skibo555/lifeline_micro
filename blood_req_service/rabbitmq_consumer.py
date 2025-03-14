import asyncio
import aio_pika
import json

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        body = json.loads(message.body)
        print(f" [x] Received {message.routing_key}: {body}")

async def consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # Declare the exchange
        exchange = await channel.declare_exchange("events_exchange", aio_pika.ExchangeType.TOPIC)

        # Declare and bind a queue (unique per service)
        queue = await channel.declare_queue("", durable=True)
        await queue.bind(exchange, routing_key="hospital.created")

        print(" [*] Waiting for events. To exit, press CTRL+C")

        await queue.consume(callback)

        # Keep the event loop running
        await asyncio.Future()

asyncio.run(consume())