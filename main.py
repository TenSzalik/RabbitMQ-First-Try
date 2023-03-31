import base64
from fastapi import FastAPI
from pymongo import MongoClient
from models import EncodedMessage
from rabbit_manager import (
    RabbitProducer,
    RabbitExchange,
    RabbitQueue,
    RabbitConsumer,
    Exchange,
    RabbitDataConnection,
    RabbitDataExchange,
    RabbitDataQueue,
    RabbitDataProducer,
    RabbitDataConsumer,
)

app = FastAPI()

creds = RabbitDataConnection(username="admin", password="admin2023", host="localhost")
exchange = RabbitDataExchange(
    exchange="exchange_1",
    exchange_type=Exchange.DIRECT,
    queue="queue_3",
    routing_key="key_1",
)
queue = RabbitDataQueue(queue="queue_1")

exchange_handler = RabbitExchange(creds=creds, exchange=exchange)
exchange_handler.create_exchange()
queue_handler = RabbitQueue(creds=creds, queue=queue)
queue_handler.create_queue()
exchange_handler.create_binding_key()

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Message"]
mongo_collection = mongo_db["encoded-message"]


@app.post("/api/send/")
async def send_message(message: EncodedMessage):
    producer = RabbitProducer(
        creds=creds,
        producer=RabbitDataProducer(
            exchange=exchange.exchange, routing_key=exchange.routing_key, body=str(message.message)
        ),
    )
    producer.send()
    return {"message": "Message sent successfully"}


@app.get("/api/receive/")
async def receive_message():
    consumer = RabbitConsumer(
        creds=creds, consumer=RabbitDataConsumer(queue=queue.queue, auto_ack=True)
    )
    body = consumer.consume_messages()
    if body:
        body = base64.b64encode(body).decode()
        mongo_collection.insert_one({"message": body})
        return {"message": body}
    return {"There is no messages in the queue"}


@app.get("/api/messages/")
async def get_messages():
    messages = []
    for doc in mongo_collection.find():
        encrypted_body = doc["message"]
        decrypted_body = base64.b64decode(encrypted_body)
        messages.append({"message": decrypted_body})
    return messages
