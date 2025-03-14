from fastapi import FastAPI
import asyncio
from rabbitmq_utils import publish_event
import aio_pika
import json

app = FastAPI()

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"

async def process_message(message):
    """Process incoming messages from RabbitMQ."""
    async with message.process():
        data = json.loads(message.body)
        matched_users = data["matched_users"]
        print(f"Sending notifications to: {matched_users}")

        # Simulating sending notifications (Email, SMS, Push)
        for user in matched_users:
            print(f"Notifying {user['user_id']} about hospital {user['hospital_id']}")

        # If needed, publish an event for another service
        event_data = {"status": "notifications_sent", "users": matched_users}
        await publish_event("notify.send", event_data)

async def consume():
    """Consume messages from RabbitMQ."""
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("match.found")
    await queue.consume(process_message)

# Run consumer in the background
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())
