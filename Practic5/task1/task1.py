from pymongo import MongoClient
import pandas as pd
import json

def create_db():
    data = pd.DataFrame(pd.read_json('./task_1_item.json'))

    client = MongoClient('localhost', 27017)
    db = client.employee_database

    if 'employee_database' not in client.list_database_names():
        collection = db.employees
        collection.insert_many(data.to_dict('records'))

    collection = db.employees

    return collection

def parse_data(collection):
    result_1 = list(collection.find({}, { '_id': 0 }).sort('salary', -1).limit(10))
    with open('result1.json', 'w', encoding='utf-8') as f:
        json.dump(result_1, f, ensure_ascii=False, indent=4)

    result_2 = list(collection.find({ 'age': {'$lt': 30} }, { '_id': 0 }).sort('salary', -1).limit(15))
    with open('result2.json', 'w', encoding='utf-8') as f:
        json.dump(result_2, f, ensure_ascii=False, indent=4)

    result_3 = list(collection.find({ '$and': [
        { 'city': 'Кишинев' },
        { 'job': { '$in': [ 'Инженер', 'Программист', 'Учитель' ]} }
    ]}, { '_id': 0 }).sort('age', 1).limit(10))
    with open('result3.json', 'w', encoding='utf-8') as f:
        json.dump(result_3, f, ensure_ascii=False, indent=4)

    collection.count_documents({})

    result_4 = collection.find(
        {
            '$and': [
                { 'age': { 'gte': 20, '$lte': 50 } },
                { 'year': { '$gte': 2019, '$lte': 2022 } },
                { '$or': [
                    { 'salary': { 'gt': 50000, '$lte': 75000 }},
                    { 'salary': { 'gt': 125000, '$lt': 150000 } },
                ]}
            ]
        },
        {'_id': 0}
    )
    print(f'Количество записей, подходящих под условие: {len(list(result_4))}')


collect = create_db()
parse_data(collect)