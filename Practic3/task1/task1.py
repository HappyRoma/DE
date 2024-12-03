import json
from collections import Counter
from bs4 import BeautifulSoup
import os
from statistics import mean


def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = BeautifulSoup(file, 'html.parser')

    category = data.find('span', text = lambda x: 'Категория' in x).get_text(strip=True).split(' ')[-1]
    title = data.find('h1', class_='book-title').get_text(strip=True)
    author = data.find('p', class_='author-p').get_text(strip=True)
    pages = int(data.find('span', class_='pages').get_text(strip=True).split(' ')[-2])
    year = int(data.find('span', class_='year').get_text(strip=True).split(' ')[-1])
    isbn =  data.find('span', text = lambda x: 'ISBN' in x).get_text(strip=True).split(':')[-1]
    rating = float(data.find('span', text = lambda x: 'Рейтинг' in x).get_text(strip=True).split(' ')[-1])
    views = int(data.find('span', text = lambda x: 'Просмотры' in x).get_text(strip=True).split(' ')[-1])

    return {
        "category": category,
        "title": title,
        "author": author,
        "pages": pages,
        "year": year,
        'isbn': isbn,
        "rating": rating,
        "views": views
    }

def parse_all_files():
    data = []
    for file in os.listdir('./1'):
        if file.endswith('.html'):
            file_path = './1/' + file
            data.append(parse_file(file_path))

    return data

def process_data(data):
    sorted_data = sorted(data, key=lambda k: k['rating'], reverse=True)

    filtered_data = [i for i in data if i['category'] == 'фэнтези']

    views = [i['views'] for i in data]
    views_stats = {
        'sum': sum(views),
        'max': max(views),
        'min': min(views),
        'mean': mean(views),
    }

    frequency_stats = Counter(item['category'] for item in data)

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "views_stats": views_stats,
        "frequency_stats": frequency_stats,
    }

def save_data(sorted_data, filtered_data, views_stats, frequency_stats):
    with open('sorted_data.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)
    with open('filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    with open('views_stats.json', 'w', encoding='utf-8') as file:
        json.dump(views_stats, file, ensure_ascii=False, indent=4)
    with open('frequency_stats.json', 'w', encoding='utf-8') as file:
        json.dump(frequency_stats, file, ensure_ascii=False, indent=4)

results = process_data(parse_all_files())

save_data(results['sorted_data'], results['filtered_data'], results['views_stats'], results['frequency_stats'])