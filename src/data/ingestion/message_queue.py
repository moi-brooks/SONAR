import pika
import json
from typing import Dict, Any, Callable
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MessageQueue:
    def __init__(self):
        self._connect()
        self._setup_queues()
    
    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            self.channel = self.connection.channel()
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def _setup_queues(self):
        # Declare queues with dead letter exchange
        self.channel.queue_declare(queue='email_ingestion', durable=True)
        self.channel.queue_declare(queue='analysis_results', durable=True)
    
    def publish_email(self, email_data: Dict[str, Any]):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='email_ingestion',
                body=json.dumps(email_data),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            logger.info(f"Published email: {email_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to publish email: {e}")
            raise
    
    def consume_emails(self, callback: Callable):
        try:
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue='email_ingestion',
                on_message_callback=callback
            )
            logger.info("Started consuming emails")
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Error in email consumption: {e}")
            raise
    
    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()