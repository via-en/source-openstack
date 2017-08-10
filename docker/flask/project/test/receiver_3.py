import pika
import os
import time
import logging.config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_DIR, 'config', 'logging.conf'))
logger = logging.getLogger(__name__)


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.exchange_declare('direct_logs', type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(queue=queue_name, exchange='direct_logs', routing_key='error')

def callback(ch, method, properties, body):
    logger.debug(" [x] Received {} from {}".format(body,method.routing_key))
    #logger.debug(" [x] done {}".format(body, ))
    #ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

logger.debug(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
#https://www.rabbitmq.com/tutorials/tutorial-four-python.html