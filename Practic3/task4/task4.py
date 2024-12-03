import json
from collections import Counter
from bs4 import BeautifulSoup
import os
from statistics import mean


# def get_tags():
#     tags = set()
#
#     file_paths = [('./4/' + file) for file in os.listdir('./4') if file.endswith('.xml')]
#
#     for file_path in file_paths:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = BeautifulSoup(file.read(), 'xml')
#             for tag in data.find_all():
#                 tags.add(tag.name)
#
#     return tags
#
# print(get_tags())

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = BeautifulSoup(file.read(), 'xml')

    clothing_items = []
    clothing_list = data.find_all('clothing')

    for clothing in clothing_list:
        id = int(clothing.find('id').get_text(strip=True)) if clothing.find('id') else None
        name = clothing.find('name').get_text(strip=True) if clothing.find('name') else None
        category = clothing.find('category').get_text(strip=True) if clothing.find('category') else None
        size = clothing.find('size').get_text(strip=True) if clothing.find('size') else None
        color = clothing.find('color').get_text(strip=True) if clothing.find('color') else None
        material = clothing.find('material').get_text(strip=True) if clothing.find('material') else None
        price = int(clothing.find('price').get_text(strip=True)) if clothing.find('price') else None
        rating = float(clothing.find('rating').get_text(strip=True)) if clothing.find('rating') else None
        reviews = int(clothing.find('reviews').get_text(strip=True)) if clothing.find('reviews') else None
        new = clothing.find('new').get_text(strip=True) if clothing.find('new') else None
        exclusive = clothing.find('exclusive').get_text(strip=True) if clothing.find('exclusive') else None
        sporty = clothing.find('sporty').get_text(strip=True) if clothing.find('sporty') else None

        clothing_items.append({
            'id': id,
            'name': name,
            'category': category,
            'size': size,
            'color': color,
            'material': material,
            'price': price,
            'rating': rating,
            'reviews': reviews,
            'new': new,
            'exclusive': exclusive,
            'sporty': sporty,
        })

    return clothing_items

def parse_all_files():
    data = []
    for file in os.listdir('./4'):
        if file.endswith('.xml'):
            file_path = './4/' + file
            data.extend(parse_file(file_path))

    return data

def process_data(data):
    sorted_data = sorted(data, key=lambda x: x['rating'] if x['rating'] is not None else int(0), reverse=True)

    filtered_data = [i for i in data if i['new'] is not None and i['new'] != '-']

    prices = [i['price'] for i in data]
    prices_stats = {
        'sum': sum(prices),
        'max': max(prices),
        'min': min(prices),
        'mean': mean(prices),
    }

    frequency_stats = Counter(i['size'] for i in data if i['size'] is not None).most_common()

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "prices_stats": prices_stats,
        "frequency_stats": frequency_stats,
    }

def save_data(sorted_data, filtered_data, prices_stats, frequency_stats):
    with open('sorted_data.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)
    with open('filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    with open('prices_stats.json', 'w', encoding='utf-8') as file:
        json.dump(prices_stats, file, ensure_ascii=False, indent=4)
    with open('frequency_stats.json', 'w', encoding='utf-8') as file:
        json.dump(frequency_stats, file, ensure_ascii=False, indent=4)

results = process_data(parse_all_files())

save_data(results['sorted_data'], results['filtered_data'], results['prices_stats'], results['frequency_stats'])