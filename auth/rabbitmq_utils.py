import json
from datetime import datetime
import aio_pika
import asyncio
from database import get_db
from models import User
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update



RABBITMQ_URL = "amqp://localhost/"

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converts datetime to a string
    raise TypeError(f"Type {type(obj)} is not serializable")


RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"
SERVICE_QUEUE_NAME = "auth_service"

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

            # if event_name == "user.logs.in":
            #     print(f"🏥 {data['data']['username']} is now online")
            # elif event_name == "request.created":
            #     print(f"🩸 New blood request created: {data['data']}")

            # elif event_name == "request.accepted":
            #     print(f"🩸 Blood request accepted: {data['data']}")

            if event_name == "hospital.created":
                print(f"🏥 New hospital registered: {data['data']}")
                db: Session = next(get_db())
                stmt = sqlalchemy_update(User).where(User.user_id == data['data']["created_by"]).values({"hospital_created": data["data"]["hospital_id"]})
                db.execute(stmt)
                db.commit()
            elif event_name == "hospital.updated":
                print(f"🏥 {data['data']['hospital_name']} has updated their details: {data['data']}")
                db: Session = next(get_db())
                stmt = sqlalchemy_update(User).where(User.user_id == data['data']["created_by"]).values(**data['data'])
                db.execute(stmt)
                db.commit()
            
            elif event_name == "hospital.deleted":
                print(f"🏥 Hospital deleted: {data['data']['hospital_name']} has deleted their hospital: {data['data']}")
                db: Session = next(get_db())
                stmt = sqlalchemy_update(User).where(User.user_id == data['data']["created_by"]).values({"hospital_created": None})
                db.execute(stmt)
                db.commit()

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
            await queue.bind(exchange, routing_key="hospital.created")
            await queue.bind(exchange, routing_key="hospital.updated")
            await queue.bind(exchange, routing_key="hospital.deleted")
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



