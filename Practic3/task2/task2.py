import json
from collections import Counter
from bs4 import BeautifulSoup
import os
from statistics import mean

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = BeautifulSoup(file, 'html.parser')

    products = []
    product_list = data.find_all('div', class_='product-item')

    for product in product_list:
        name = product.find('span').get_text(strip=True)
        price = int(product.find('price').get_text(strip=True).replace(' ','').replace('₽',''))
        id = product.find('a', class_='add-to-favorite')['data-id'] if product.find('a', class_='add-to-favorite') else None
        image_link = product.find('img')['src'] if product.find('img') else None
        bonuses = int(product.find('strong').get_text(strip=True).split(' ')[-2]) if product.find('strong') else None
        processor = product.find('li', type='processor').get_text(strip=True) if product.find('li', type='processor') else None
        ram = product.find('li', type='ram').get_text(strip=True) if product.find('li', type='ram') else None
        sim = product.find('li', type='sim').get_text(strip=True) if product.find('li', type='sim') else None
        matrix = product.find('li', type='matrix').get_text(strip=True) if product.find('li', type='matrix') else None
        resolution = product.find('li', type='resolution').get_text(strip=True) if product.find('li', type='resolution') else None
        camera = product.find('li', type='camera').get_text(strip=True) if product.find('li', type='camera') else None
        acc = product.find('li', type='acc').get_text(strip=True) if product.find('li', type='acc') else None

        products.append({
            "name": name,
            "price": price,
            "id": id,
            "image_link": image_link,
            "bonuses": bonuses,
            "processor": processor,
            "ram": ram,
            "sim": sim,
            "matrix": matrix,
            "resolution": resolution,
            "camera": camera,
            "acc": acc,
        })

    return products

def parse_all_files():
    data = []
    for file in os.listdir('./2'):
        if file.endswith('.html'):
            file_path = './2/' + file
            data.extend(parse_file(file_path))

    return data

def process_data(data):
    sorted_data = sorted(data, key=lambda x: x['bonuses'] if x['bonuses'] is not None else int(0), reverse=True)

    filtered_data = [i for i in data if i['sim'] is not None]

    prices = [i['price'] for i in data]
    prices_stats = {
        'sum': sum(prices),
        'max': max(prices),
        'min': min(prices),
        'mean': mean(prices),
    }

    frequency_stats = Counter(i['ram'] for i in data if i['ram'] is not None).most_common()

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