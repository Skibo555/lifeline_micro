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
        message_body = json.dumps({"event": event_name, "data": data}, default=json_serializer)

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

        # if event_name == "user.created":
        #     print(f"👤 New user registered: {data['data']}")
        if event_name == "user.logs.in":
            print(f"🏥 {data['data']['username']} is now online: {data['data']}")
        # elif event_name == "request.created":
        #     print(f"🩸 New blood request created: {data['data']}")

        elif event_name == "request.accepted":
            print(f"🩸 Blood request accepted: {data['data']}")

        elif event_name == "hospital.created":
            print(f"🏥 New hospital registered: {data['data']}")
            db: Session = next(get_db())
            stmt = sqlalchemy_update(User).where(User.user_id == data['data']["created_by"]).values({"hospital_created": data["data"]["hospital_id"]})
            db.execute(stmt)
            db.commit()
        elif event_name == "hospital.updated":
            print(f"🏥 {data['data']['hospital_name']} has updated their details: {data['data']}")
        
        elif event_name == "hospital.deleted":
            print(f"🏥 Hospital deleted: {data['data']['hospital_name']} has deleted their hospital: {data['data']}")
            db: Session = next(get_db())
            stmt = sqlalchemy_update(User).where(User.user_id == data['data']["created_by"]).values({"hospital_created": None})
            db.execute(stmt)
            db.commit()


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
    # await queue.bind(exchange, routing_key="user.created")
    # await queue.bind(exchange, routing_key="request.created")
    await queue.bind(exchange, routing_key="hospital.created")
    await queue.bind(exchange, routing_key="hospital.updated")
    await queue.bind(exchange, routing_key="hospital.deleted")
    await queue.bind(exchange, routing_key="user.logs.in")
    # await queue.bind(exchange, routing_key="request.accepted")
    # await queue.bind(exchange, routing_key="request.cancelled")




    # Start consuming messages
    await queue.consume(process_message)

    print(" [*] Waiting for events in Authentication Service...")
    await asyncio.Future()  # Keep running forever

if __name__ == "__main__":
    asyncio.run(consume())  # Run consumer



