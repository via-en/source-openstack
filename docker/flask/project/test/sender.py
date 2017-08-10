import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

task = ['1', '2', '3', '4']

for i in task:
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=i,
                          properties=pika.BasicProperties(
                              delivery_mode=2,)
                          )
connection.close()
#https://www.rabbitmq.com/tutorials/tutorial-two-python.html