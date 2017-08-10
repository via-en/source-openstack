import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.exchange_declare('logs', type='fanout')

task = ['1', '2', '3', '4']

for i in task:
    channel.basic_publish(exchange='logs',
                          body=i,
                          routing_key='',
                          properties=pika.BasicProperties(
                              delivery_mode=2, )
                          )
channel.close()
connection.close()
#https://www.rabbitmq.com/tutorials/tutorial-three-python.html
