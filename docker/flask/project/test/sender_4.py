import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.exchange_declare('direct_logs', type='direct')

task = {'info': ['info-1', 'info-2', 'info-3', 'info-4'], 'warning': ['warning-1', 'warning-2'], 'error': ['error-3', 'error-4']}

severitis = ['info', 'warning', 'error']

for severity in severitis:
    for i in task[severity]:
        channel.basic_publish(exchange='direct_logs',
                              body=i,
                              routing_key=severity,
                              properties=pika.BasicProperties(
                                  delivery_mode=2, )
                              )
channel.close()
connection.close()
#https://www.rabbitmq.com/tutorials/tutorial-three-python.html
