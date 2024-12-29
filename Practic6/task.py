import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

dataFrame = pd.read_csv('./crime-data.csv')

# Анализ данных
def analyse_memory(data):
    total_memory = data.memory_usage(deep=True).sum()
    memory_per_column = data.memory_usage(deep=True)

    memory_stats = {
        'total_memory':  int(total_memory),
        'columns': []
    }
    for column in data.columns:
        column_memory = memory_per_column[column].sum()
        memory_stats['columns'].append({
            'column': column,
            'memory': int(column_memory),
            'percentage': float(column_memory / total_memory),
            'dtype': str(data.dtypes[column])
        })

    return memory_stats

default_memory_stats = analyse_memory(dataFrame)
with open('./default_memory_stats.json', 'w') as f:
    json.dump(default_memory_stats, f)

# Преобразование данных
def process_data(data):
    for column in data.select_dtypes(include=['object']):
        if data[column].nunique() / len(data[column]) < 0.5:
            data[column] = data[column].astype('category')

    for column in data.select_dtypes(include=['int']).columns:
        data[column] = pd.to_numeric(data[column], downcast='integer')

    for column in data.select_dtypes(include=['float']).columns:
        data[column] = pd.to_numeric(data[column], downcast='float')

    return data

optimized_data = process_data(dataFrame)
optimized_memory_stats = analyse_memory(optimized_data)
with open('./optimized_memory_stats.json', 'w') as f:
    json.dump(optimized_memory_stats, f)

chunk_size = 50000
selected_columns = ['DR_NO', 'Date Rptd', 'AREA NAME', 'Crm Cd Desc', 'Vict Age', 'Vict Sex', 'Status', 'Weapon Desc']
selected_data = []
for chunk in pd.read_csv('./crime-data.csv', usecols=selected_columns, chunksize=chunk_size):
    chunk = process_data(chunk)
    selected_data.append(chunk)

final_data = pd.concat(selected_data)
final_data.to_csv('./final_data.csv', index=False)

# Построение графиков
df = pd.read_csv('./final_data.csv')
graphics_folder = './graphics'

# 1. Столбчатая: Количество преступлений по типу оружия
plt.figure(figsize=(16, 20))
weapon_counts = df['Weapon Desc'].value_counts().head(10)
weapon_counts.plot(kind='bar',x=weapon_counts.values, y=weapon_counts.index)
plt.title('Количество преступлений по типу оружия')
plt.xlabel('Тип оружия')
plt.ylabel('Количество')
plt.savefig(graphics_folder+'/weapon_count')
plt.show()

# 2. .Круговая: Распределение преступлений по полу жертвы
plt.figure(figsize=(8, 8))
gender_distribution = df['Vict Sex'].value_counts().head(3)
plt.pie(gender_distribution, labels=gender_distribution.index, autopct='%1.1f%%', startangle=140)
plt.title('Распределение по полу жертв')
plt.savefig(graphics_folder+'/gender_distribution')
plt.show()

# 3. Линейная: Средний возраст жертв по годам
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'])
avg_age_by_year = df.groupby(df['Date Rptd'].dt.year)['Vict Age'].mean()
plt.figure(figsize=(10, 6))
plt.plot(avg_age_by_year.index, avg_age_by_year.values, marker='o', linestyle='-', color='b')
plt.title('Средний возраст жертв по годам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Средний возраст', fontsize=12)
plt.grid()
plt.savefig(graphics_folder+'/avg_age_by_year')
plt.show()

# 4. Гистограмма: Распределение возраста жертв
plt.figure(figsize=(10, 6))
plt.hist(df['Vict Age'].dropna(), bins=30, color='purple', alpha=0.7)
plt.title('Распределение возраста жертв', fontsize=14)
plt.xlabel('Возраст', fontsize=12)
plt.ylabel('Частота', fontsize=12)
plt.grid()
plt.savefig(graphics_folder+'/age_distribution')
plt.show()

# 5. Самые частые типы преступлений
plt.figure(figsize=(12, 20))
crime_counts = df['Crm Cd Desc'].value_counts().head(10)
crime_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Самые частые типы преступлений', fontsize=14)
plt.xlabel('Тип преступления', fontsize=12)
plt.ylabel('Количество', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid()
plt.savefig(graphics_folder+'/freqency_distribution')
plt.show()
