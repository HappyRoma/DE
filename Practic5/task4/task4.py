import pandas as pd
from pymongo import MongoClient
import json

def sampling_data():
    # Сэмплим данные, чтобы получить +-400Mb -> +-40mb
    data = pd.DataFrame(pd.read_csv('./student_assessment_performance.csv'))
    sampled_data = data.sample(frac=0.1)
    sampled_data.to_csv('sampled_data.csv')

def insert_data(collection):
    data = pd.DataFrame(pd.read_csv('./sampled_data.csv'))
    collection.insert_many(data.to_dict('records'))

def find_data(collection):

    result_1 = list(collection.find({
        "District": "Capital School District",
        "RowStatus": "REPORTED"
    }, { '_id': 0 }).limit(10))
    with open('./results1/result_1.json', 'w', encoding='utf-8') as f:
        json.dump(result_1, f, ensure_ascii=False, indent=4)

    result_2 = list(collection.find({
        "ScaleScoreAvg": {"$gt": 2000},
        "Tested": {"$gt": 15},
    }, { '_id': 0 }).sort("ScaleScoreAvg", 1).limit(10))
    with open('./results1/result_2.json', 'w', encoding='utf-8') as f:
        json.dump(result_2, f, ensure_ascii=False, indent=4)

    result_3 = list(collection.find({
        "Gender": "Male",
        "Proficient": {"$gt": 10}
    }, { '_id': 0 }).limit(10))
    with open('./results1/result_3.json', 'w', encoding='utf-8') as f:
        json.dump(result_3, f, ensure_ascii=False, indent=4)

    result_4 = list(collection.find({
        "Race": "Hispanic/Latino",
        "Grade": "8th Grade",
        "RowStatus": "REPORTED"
    }, { '_id': 0 }).limit(10))
    with open('./results1/result_4.json', 'w', encoding='utf-8') as f:
        json.dump(result_4, f, ensure_ascii=False, indent=4)

    result_5 = list(collection.find({
        "Tested": {"$gt": 25},
        "RowStatus": "REDACTED"
    }, { '_id': 0 }).limit(10))
    with open('./results1/result_5.json', 'w', encoding='utf-8') as f:
        json.dump(result_5, f, ensure_ascii=False, indent=4)


def find_with_aggregation(collection):
    # Мин, Макс, Ср балл по каждому учебному году
    result_1 = list(collection.aggregate([
        {
            "$match": {
                "ScaleScoreAvg": {"$ne": float("NaN")},
            }
        },
        {
            "$group": {
                "_id": "$School Year",
                "min_score": {"$min": "$ScaleScoreAvg"},
                "max_score": {"$max": "$ScaleScoreAvg"},
                "avg_score": {"$avg": "$ScaleScoreAvg"},
            }
        }
    ]))
    with open('./results2/result_1.json', 'w', encoding='utf-8') as f:
        json.dump(result_1, f, ensure_ascii=False, indent=4)

    # Количество записей для каждого RowStatus
    result_2 = list(collection.aggregate([
        {
            "$group": {
                "_id": "$RowStatus",
                "count": {"$sum": 1},
            }
        }
    ]))
    with open('./results2/result_2.json', 'w', encoding='utf-8') as f:
        json.dump(result_2, f, ensure_ascii=False, indent=4)

    # Топ 10 школ по среднему рейтенгу за все года
    result_3 = list(collection.aggregate([
        {
            "$match": {
                "ScaleScoreAvg": {"$ne": float("NaN")},
            }
        },
        {
            "$sort": {"ScaleScoreAvg": -1}
        },
        {
            "$limit": 10
        },
        {
            "$project": {"_id": 0, "Organization": 1, "District Code": 1, "ScaleScoreAvg": 1, "School Year": 1}
        }
    ]))
    with open('./results2/result_3.json', 'w', encoding='utf-8') as f:
        json.dump(result_3, f, ensure_ascii=False, indent=4)

    # Среднее количество сдавших среди мужчин
    result_4 = list(collection.aggregate([
        {
            "$match": {
                "PctProficient": {"$ne": float("NaN")},
            }
        },
        {
            "$group": {
                "_id": "$Gender",
                "avg_score": {"$avg": "$PctProficient"},
            }
        }
    ]))
    with open('./results2/result_4.json', 'w', encoding='utf-8') as f:
        json.dump(result_4, f, ensure_ascii=False, indent=4)

    # Средний балл среди белых по классам
    result_5 = list(collection.aggregate([
        {
            "$match": {
                "Race": "White",
                "ScaleScoreAvg": {"$ne": float("NaN")},
            }
        },
        {
            "$group": {
                "_id": "$Grade",
                "avg_score": {"$avg": "$ScaleScoreAvg"},
            }
        },
        {
            "$sort": {"avg_score": -1}
        }
    ]))
    with open('./results2/result_5.json', 'w', encoding='utf-8') as f:
        json.dump(result_5, f, ensure_ascii=False, indent=4)

def update_delete_data(collection):
    # Удалить все записи, где процент успешно сдавших меньше 5
    collection.delete_many(
        {"PctProficient": {"$lt": 5}}
    )

    # Повысить на 10% средний бал для записей 2022 со статусом Reported
    collection.update_many(
        {"School Year": 2022, "RowStatus": "REPORTED"},
        {"$mul": {"ScaleScoreAvg": 1.1}}
    )

    # Обновить статус у записей с менее 20 протестированными учениками
    collection.update_many(
        {"Tested": {"$lt": 20}},
        {"$set": {"RowStatus": "REDACTED"}}
    )

    # Обновить у всех записей Race: African American PctProficient на 5
    collection.update_many(
        {"Race": "African American"},
        {"$inc": {"PctProficient": 5}}
    )

    # Удалить все записи мужского пола с успешно сданными меньше 10
    collection.delete_many(
        {
            "Gender": "Male",
            "Proficient": {"$lte": 10}
        }
    )




client = MongoClient('localhost', 27017)
db = client.education_database
collect = db.student_assessments

find_data(collect)
find_with_aggregation(collect)
update_delete_data(collect)

# insert_data(collect)