from numpy.ma.core import resize
from pymongo import MongoClient
import pandas as pd
import json

def parse_data():
    data = []
    with open('./task_2_item.text', 'r', encoding='utf-8') as f:
        content = f.read()

        for person in content.split('====='):

            person = person.strip()
            person_data = {}

            if person:
                for line in person.split('\n'):
                    key, value = line.split('::')
                    value = value.strip()
                    if key in [ "age", "id", "salary", "year" ]:
                        value = int(value)
                    person_data[key.strip()] = value
                data.append(person_data)

    return data

def insert_data(collection, data):
    collection.insert_many(data)

def analyse_db(collection):

    # Вывод минимальной, средней, максимальной salary
    result_1 = list(collection.aggregate([
        {
            "$group": {
                "_id": None,
                "min_salary": { "$min": "$salary" },
                "max_salary": { "$max": "$salary" },
                "avg_salary": { "$avg": "$salary" },
            }
        }
    ]))
    with open('result1.json', 'w', encoding='utf-8') as f:
        json.dump(result_1, f, ensure_ascii=False, indent=4)

    # вывод количества данных по представленным профессиям
    result_2 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "count": { "$sum": 1 },
            }
        }
    ]))
    with open('result2.json', 'w', encoding='utf-8') as f:
        json.dump(result_2, f, ensure_ascii=False, indent=4)

    # вывод минимальной, средней, максимальной salary по городу
    result_3 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "min_salary": { "$min": "$salary" },
                "max_salary": { "$max": "$salary" },
                "avg_salary": { "$avg": "$salary" },
            }
        }
    ]))
    with open('result3.json', 'w', encoding='utf-8') as f:
        json.dump(result_3, f, ensure_ascii=False, indent=4)

    # вывод минимальной, средней, максимальной salary по профессии
    result_4 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "min_salary": { "$min": "$salary" },
                "max_salary": { "$max": "$salary" },
                "avg_salary": { "$avg": "$salary" },
            }
        }
    ]))
    with open('result4.json', 'w', encoding='utf-8') as f:
        json.dump(result_4, f, ensure_ascii=False, indent=4)

    # вывод минимального, среднего, максимального возраста по городу
    result_5 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$city",
                "min_age": { "$min": "$age" },
                "max_age": { "$max": "$age" },
                "avg_age": { "$avg": "$age" },
            }
        }
    ]))
    with open('result5.json', 'w', encoding='utf-8') as f:
        json.dump(result_5, f, ensure_ascii=False, indent=4)

    # вывод минимального, среднего, максимального возраста по профессии
    result_6 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$job",
                "min_age": { "$min": "$age" },
                "max_age": { "$max": "$age" },
                "avg_age": { "$avg": "$age" },
            }
        }
    ]))
    with open('result6.json', 'w', encoding='utf-8') as f:
        json.dump(result_6, f, ensure_ascii=False, indent=4)

    # вывод максимальной заработной платы при минимальном возрасте
    result_7 = list(collection.aggregate([
        {
            "$group": {
                "_id": None,
                "min_age": { "$min": "$age" },
            }
        },
        {
            "$lookup": {
                "from": "employees",
                "localField": "min_age",
                "foreignField": "age",
                "as": "data"
            }
        },
        {
            "$unwind": "$data"
        },
        {
            "$project": {
                "data._id": 0
            }
        },
        {
            "$sort": {"data.salary": -1}
        },
        {
            "$limit": 1
        }
    ]))
    with open('result7.json', 'w', encoding='utf-8') as f:
        json.dump(result_7, f, ensure_ascii=False, indent=4)

    # вывод минимальной заработной платы при максимальной возрасте
    result_8 = list(collection.aggregate([
        {
            "$group": {
                "_id": None,
                "max_age": { "$max": "$age" },
            }
        },
        {
            "$lookup": {
                "from": "employees",
                "localField": "max_age",
                "foreignField": "age",
                "as": "data"
            }
        },
        {
            "$unwind": "$data"
        },
        {
            "$project": {
                "data._id": 0
            }
        },
        {
            "$sort": {"data.salary": 1}
        },
        {
            "$limit": 1
        }
    ]))
    with open('result8.json', 'w', encoding='utf-8') as f:
        json.dump(result_8, f, ensure_ascii=False, indent=4)

    # вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по убыванию по полю avg
    result_9 = list(collection.aggregate([
        {
            "$match": { "salary": { "$gte": 50000 }},
        },
        {
            "$group": {
                "_id": "$city",
                "min_salary": { "$min": "$salary" },
                "max_salary": { "$max": "$salary" },
                "avg_salary": { "$avg": "$salary" },
            }
        },
        { "$sort": { "avg_age": -1 }}
    ]))
    with open('result9.json', 'w', encoding='utf-8') as f:
        json.dump(result_9, f, ensure_ascii=False, indent=4)

    # вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту
    result_10 = list(collection.aggregate([
        {
            "$match": {
                "$or": [
                    { "age": { "$gt": 18, "$lt": 25 }},
                    { "age": { "$gt": 50, "$lt": 65 }},
                ]
            }
        },
        {
            "$group": {
                "_id": { "city": "$city", "job": "$job" },
                "min_salary": { "$min": "$salary" },
                "max_salary": { "$max": "$salary" },
                "avg_salary": { "$avg": "$salary" },
            }
        }
    ]))
    with open('result10.json', 'w', encoding='utf-8') as f:
        json.dump(result_10, f, ensure_ascii=False, indent=4)

    # подсчет количества работников старше 25, отсортированных по убыванию средней ЗП
    result_11 = list(collection.aggregate([
        {
            "$match": {
                "age": { "$gt": 25 }
            }
        },
        {
            "$group": {
                "_id": "$job",
                "total_employees": { "$sum": 1 },
                "avg_salary": { "$avg": "$salary" },
            }
        },
        {
            "$sort": { "avg_salary": -1}
        }
    ]))
    with open('result11.json', 'w', encoding='utf-8') as f:
        json.dump(result_11, f, ensure_ascii=False, indent=4)


client = MongoClient('localhost', 27017)
db = client.employee_database
collect = db.employees
analyse_db(collect)

# insert_data(collection, parse_data())

