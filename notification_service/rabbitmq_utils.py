import json
import asyncio
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


async def process_matched_donor(message: aio_pika.IncomingMessage):
    """Process blood match event and update request."""
    async with message.process():
        data = json.loads(message.body)
        print(f" [x] Matched Donor Found: {data}")

        # Example: Update the blood request in the database
        request_id = data.get("request_id")
        donor_id = data.get("donor_id")
        print(f"Updating blood request {request_id} with donor {donor_id}")

async def consume_events():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # Declare exchange
        exchange = await channel.declare_exchange("events_exchange", aio_pika.ExchangeType.TOPIC)

        # Declare queue and bind to "blood_request.matched"
        queue = await channel.declare_queue("", durable=True)
        await queue.bind(exchange, routing_key="blood_request.matched")

        print(" [*] Waiting for matched blood donors...")

        # Consume messages
        await queue.consume(process_matched_donor)

        await asyncio.Future()  # Keep listening

asyncio.run(consume_events())
