import json
import aio_pika
import asyncio

RABBITMQ_URL = "amqp://localhost/"

async def publish_event(event_name: str, data: dict, exchange_name: str = "events"):
    """
    Publishes an event to a RabbitMQ exchange (direct exchange).
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # Declare exchange (direct type)
        exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)

        # Convert message to JSON
        message_body = json.dumps({"event": event_name, "data": data})

        # Publish message with routing key (event_name)
        await exchange.publish(
            aio_pika.Message(body=message_body.encode(), content_type="application/json"),
            routing_key=event_name  # Direct exchange uses routing key
        )

        print(f"✅ Published event '{event_name}' to exchange '{exchange_name}'")


async def process_message(message: aio_pika.IncomingMessage):
    """
    Async function to process incoming messages.
    """
    async with message.process():  # Auto-acknowledge after processing
        body = message.body.decode()
        data = json.loads(body)

        event_name = message.routing_key  # Get event type

        if event_name == "user.created":
            print(f"👤 New user registered: {data['data']}")
        elif event_name == "blood.request.created":
            print(f"🩸 New blood request: {data['data']}")
        elif event_name == "hospital.created":
            print(f"🏥 New hospital registered: {data['data']}")

async def consume():
    """
    Async consumer to listen for events.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    # Declare exchange
    exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.DIRECT)

    # Declare queue
    queue = await channel.declare_queue("event_queue", durable=True)

    # Bind queue to exchange with routing keys for specific events
    await queue.bind(exchange, routing_key="user.created")
    await queue.bind(exchange, routing_key="blood.request.created")
    await queue.bind(exchange, routing_key="hospital.created")

    # Start consuming messages
    await queue.consume(process_message)

    print(" [*] Waiting for events in Notification Service...")
    await asyncio.Future()  # Keep running forever

if __name__ == "__main__":
    asyncio.run(consume())  # Run consumer

