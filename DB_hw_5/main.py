import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale

def get_file_path(file_name):
    return os.path.join(os.getcwd(), file_name)

def entering_data(file_path, session):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        model = item.get('model').capitalize()
        session.add(eval(model)(id=item.get('pk'), **item.get('fields')))
    session.commit()

def getting_data(publisher_input, session):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
                   .join(Publisher, Book.publisher)\
                   .join(Stock, Book.stocks)\
                   .join(Shop, Stock.shop)\
                   .join(Sale, Stock.sales)

    if publisher_input.isdigit():
        query = query.filter(Publisher.id == int(publisher_input))
    else:
        query = query.filter(Publisher.name == publisher_input)

    results = query.all()

    if results:
        for book, shop, price, date in results:
            print(f'{book:40}| {shop:10}| {price:8}| {date.strftime("%d-%m-%Y")}|')
    else:
        print('Такого издателя нет в базе!')

if __name__ == '__main__':
    login = input('Введите имя пользователя: ')
    password = input('Введите пароль: ')
    host = input('Введите host сервера: ')
    port = input('Введите порт сервера: ')
    name_db = input('Введите название БД: ')

    DSN = f'postgresql://{login}:{password}@{host}:{port}/{name_db}'

    engine = sqlalchemy.create_engine(DSN)
    file_path = get_file_path('tests_data.json')
    publisher_input = input('Введите имя или id издателя: ')

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        create_tables(engine)
        entering_data(file_path, session)
        getting_data(publisher_input, session)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        session.close()
