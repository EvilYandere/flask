import json

import pika

from main import Product, db

params = pika.URLParameters('amqps://zgjdnemk:mazfHa2ilWv0vBaI6g3jeDRQODDeLtTA@fish.rmq.cloudamqp.com/zgjdnemk')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Получил сообщение')
    data = json.loads(body)

    print(data)

    if properties.content_type == 'Создал продукт':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Создал продукт')

    elif properties.content_type == 'Обновил продукт':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Обновил продукт')

    elif properties.content_type == 'Удалил продукт':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Удалил продукт')



channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

channel.start_consuming()

channel.close()
