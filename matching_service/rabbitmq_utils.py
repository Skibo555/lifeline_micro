import json
from datetime import datetime
import aio_pika
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from rabbitmq_service.communications.rabbitmq_publisher import rabbitmq_service
from database import get_db
from models import User
from sqlalchemy.orm import Session
from matcher import find_nearest_users

RABBITMQ_URL = "amqp://localhost/"
EXCHANGE_NAME = "events"
SERVICE_QUEUE_NAME = "matching_service"


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

            # print(f"📩 Received event: {event_name}, Data: {data}")
            if event_name == "user.created":
                print(f"👤 New user registered: {data['data']}")
                db: Session = next(get_db())
                user = User(**data['data'])
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"👤 User added to database: {user}")

            elif event_name == "user.updated":
                print(f"👤 A user updated their details: {data['data']}")
            elif event_name == "user.deleted":
                print(f"👤 A user just deleted their account: {data['data']}")
            elif event_name == "request.created":
                print(f"🩸 New blood request created: {data['data']}")
                db: Session = next(get_db())
                users = db.query(User).all()
                if not users:
                    return "No users found!"
                # print(type(users))
                users_dict = [{key: value for key, value in user.__dict__.items() if not key.startswith('_')} for user in users]

                users_nearby = find_nearest_users(request_lat=data['data']['lat'], request_long=data['data']['long'], users=users_dict)
                print(users_nearby)
                # json_format = json.dumps({"data": users_nearby}, default=json_serializer)
                await rabbitmq_service.publish_event(event_name="match.found", data=users_nearby)

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

            
            # Bind queue to exchange with routing keys for specific events
            await queue.bind(exchange, routing_key="user.created")
            await queue.bind(exchange, routing_key="user.updated")
            await queue.bind(exchange, routing_key="user.deleted")
            await queue.bind(exchange, routing_key="request.created")
            await queue.bind(exchange, routing_key="hospital.created")

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


