import msgpack
from pymongo import MongoClient


def fill_db(connection):
    with open("task_3_item.msgpack", "rb") as f:
        data = msgpack.load(f)

    connection.insert_many(data)


def delete_data(collection):
    # удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
    collection.delete_many({
        "$or": [
            { "salary": { "$lt": 25000 }},
            { "salary": { "$gt": 175000 } }
        ]
    })

    # увеличить возраст (age) всех документов на 1
    collection.update_many(
        {},
        {"$inc": {"age": 1}}
    )

    # поднять заработную плату на 5% для произвольно выбранных профессий
    collection.update_many(
        { "job": { "$in": [ "Инженер", "IT-специалист" ]}},
        { "$mul": { "salary": 1.05 }}
    )

    # поднять заработную плату на 7% для произвольно выбранных городов
    collection.update_many(
        { "city": { "$in": [ "Прага", "Кордова" ]}},
        { "$mul": { "salary": 1.07 }}
    )

    # поднять заработную плату на 10% для выборки по сложному предикату
    collection.update_many(
        {
            "$and": [
                { "city": "Хельсинки"},
                { "job": {"$in": ["Водитель", "Врач"]}},
                { "age": { "$gte": 50 }}
            ]
        },
        { "$mul": { "salary": 1.10 }}
    )

    # удалить из коллекции записи по произвольному предикату
    collection.delete_many(
        {
            "$and": [
                { "age": { "$gte": 60 }},
                { "city": "Сараево"}
            ]
        }
    )

client = MongoClient('localhost', 27017)
db = client.employee_database
collect = db.employees

delete_data(collect)

# fill_db(collect)