import pika
import os, sys
import logging.config
sys.path.append(os.getcwd())
from config import Config


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)
params = Config.setup_main_config(os.path.join(config_path, 'main.yml'))

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
#https://www.rabbitmq.com/tutorials/tutorial-three-python.html