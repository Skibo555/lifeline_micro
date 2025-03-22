import json
import aio_pika
import asyncio

RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"
SERVICE_QUEUE_NAME = "notification_service"

async def publish_event(event_name: str, data: dict):
    """
    Publishes an event to the RabbitMQ exchange.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True)

        message_body = json.dumps({"event": event_name, "data": data})

        await exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=event_name  
        )

        print(f"✅ Published event '{event_name}'")


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
