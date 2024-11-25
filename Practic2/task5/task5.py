import msgpack
import pandas as pd
import numpy as np
import json
import pickle
import os

data = pd.read_csv('crime_data.csv')

# Уменьшение количества данных для достижения нужного размера файла

# reduced_data = data[:len(data) // 7]
# reduced_data.to_csv('crime_data.csv', index=False)

selected_fields = [
    'Date Rptd', # Дата подачи отчета
    'DATE OCC', # ДАта совершения преступления
    'TIME OCC', # Время совершения преступления
    'AREA NAME', # Район
    'Vict Age', # Возраст жертвы
    'Vict Sex', # Пол жертвы
    'Premis Desc', # Место происшествия
    'Weapon Desc' # Оружие
]

data=data[selected_fields]

def numeric_analysis():
    numeric_columns = ['TIME OCC', 'Vict Age']
    numeric_stats = {
        col: {
            'max': int(data[col].max()),
            'min': int(data[col].min()),
            'mean': float(data[col].mean()),
            'sum': int(data[col].sum()),
            'std': float(data[col].std())
        }
        for col in numeric_columns
    }

    return numeric_stats

def string_analysis():
    string_columns = ['AREA NAME', 'Vict Sex', 'Premis Desc', 'Weapon Desc', 'Date Rptd', 'DATE OCC']
    string_stats = {
        col: data[col].value_counts().to_dict() for col in string_columns
    }
    return string_stats

result = {
    'numeric_stats': numeric_analysis(),
    'string_stats': string_analysis()
}

with open('result.json', "w", encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

data.to_csv('processed_data.csv')
data.to_json('processed_data.json')
with open('processed_data.msgpack', 'wb') as f:
    msgpack.pack(data.to_dict(), f)
with open('processed_data.pkl', 'wb') as f:
    pickle.dump(data, f)


print(f"Размер файла csv: { os.path.getsize('processed_data.csv')} ")
print(f"Размер файла json: { os.path.getsize('processed_data.json'),} ")
print(f"Размер файла msgpack: { os.path.getsize('processed_data.msgpack')} ")
print(f"Размер файла pkl: { os.path.getsize('processed_data.pkl')} ")