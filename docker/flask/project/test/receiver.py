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
channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    logger.debug(" [x] Received {}".format(body,))
    time.sleep(2)
    logger.debug(" [x] done {}".format(body, ))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue',
                      no_ack=False)

logger.debug(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
#https://www.rabbitmq.com/tutorials/tutorial-two-python.html