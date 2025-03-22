import json
import aio_pika
import asyncio

from email_sender.send import send_email

RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"
SERVICE_QUEUE_NAME = "notification_service"


async def process_message(message: aio_pika.IncomingMessage):
    """
    Processes incoming RabbitMQ messages.
    """
    async with message.process():  
        try:
            body = message.body.decode()
            data = json.loads(body)
            event_name = message.routing_key  

            # print(f"📩 [{SERVICE_QUEUE_NAME}] Received event: {event_name}, Data: {data}")
            if event_name == "match.found":
                # print(f"🩸 Match found for user: {data["data"]}")
                print(f"This is the lenght of the object {len(data["data"])}")
                for user in data["data"]:
                    await send_email(user)
                    print(f"🩸 Notifying user: {user["username"]}")
                

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
