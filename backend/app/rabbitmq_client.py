import os
import json
import pika
from pika.exceptions import AMQPError
from app.config import RABBIT_URL

def _connect():
    params = pika.URLParameters(RABBIT_URL)
    return pika.BlockingConnection(parameters=params)

def publish(queue: str, message: dict) -> None:
    conn = None
    try:
        print(message)
        conn = _connect()
        ch = conn.channel()
        # Declare the queue (idempotent) to ensure it exists
        ch.queue_declare(queue=queue, durable=True)
        body = json.dumps(message)
        props = pika.BasicProperties(
                delivery_mode=2, 
            )
        ch.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
            properties=props,
        )
    except AMQPError as e:
        print("ERORRRRR")
        raise
    finally:
        if conn and not conn.is_closed:
            conn.close()
