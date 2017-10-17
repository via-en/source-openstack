import pika
import os, sys
import logging.config
import time
sys.path.append(os.getcwd())
from config import Config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)
params = Config.setup_main_config(os.path.join(config_path, 'main.yml'))

connection = pika.BlockingConnection(pika.ConnectionParameters(params.receiver.host))
channel = connection.channel()

queue = params.receiver.queue.social

channel.queue_declare(queue=queue, durable=True)
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    logger.debug(" [x] Received {} from {}".format(body,method.routing_key))
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_consume(callback,
                      queue=queue,
                      no_ack=False)

logger.debug(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
#https://www.rabbitmq.com/tutorials/tutorial-three-python.html
