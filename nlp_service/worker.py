from dotenv import load_dotenv
import os
import logging
import signal
import json
import random
import pika
import sys

load_dotenv(".env")
RABBIT_URL = os.getenv("RABBITMQ_URL")
IN_QUEUE = "reviews_for_nlp"
OUT_QUEUE = "nlp_results"

logging.basicConfig(level=logging.INFO)
# logging.getLogger("pika").setLevel(logging.WARNING)
logger = logging.getLogger("nlp-worker")

should_exit = False
def on_shutdown(sig, frame):
    global should_exit
    should_exit = True

signal.signal(signal.SIGINT, on_shutdown)
signal.signal(signal.SIGTERM, on_shutdown)

logger.info("Connecting to RabbitMQ at %s", RABBIT_URL)
conn = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
ch   = conn.channel()
ch.queue_declare(queue=IN_QUEUE,  durable=True)
ch.queue_declare(queue=OUT_QUEUE, durable=True)
ch.basic_qos(prefetch_count=1)

def on_message(ch, method, props, body):
    msg = json.loads(body)
    review_id = msg["review_id"]
    restaurant_id = msg["restaurant_id"]
    text = msg["text"]

    logger.info(f"Analyzing review={review_id}")
    try:
        sentiment = random.choice(["POSITIVE", "NEGATIVE"])
        confidence = random.random()
        
        prop = pika.BasicProperties(delivery_mode=2)
        ch.basic_publish(
            exchange="",
            routing_key=OUT_QUEUE,
            body=json.dumps({
                "review_id": review_id,
                "restaurant_id": restaurant_id,
                "sentiment": sentiment,
                "confidence": confidence
            }),
            properties=prop
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Published NLP result for review={review_id}")

    except Exception:
        logger.exception(f"Failed to process review={review_id}, requeueing")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    ch.basic_consume(queue=IN_QUEUE, on_message_callback=on_message)

    logger.info("NLP worker listening on reviews_for_nlp…")
    while not should_exit:
        conn.process_data_events(time_limit=1)

    logger.info("🛑 Shutdown signal received, closing connection…")
    conn.close()
    sys.exit(0)
    ch.start_consuming()

if __name__ == "__main__":
    main()