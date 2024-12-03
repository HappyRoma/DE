import json
from collections import Counter
from bs4 import BeautifulSoup
import os
from statistics import mean

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        star = BeautifulSoup(file.read(), 'xml').star

    name = star.find('name').get_text(strip=True) if star.find('name') else None
    constellation = star.find('constellation').get_text(strip=True) if star.find('constellation') else None
    spectral = star.find('spectral-class').get_text(strip=True) if star.find('spectral-class') else None
    radius = int(star.find('radius').get_text(strip=True)) if star.find('radius') else None
    rotation = float(star.find('rotation').get_text(strip=True).replace(' days', '')) if star.find('rotation') else None
    age = float(star.find('age').get_text(strip=True).replace(' billion years', '')) if star.find('age') else None
    distance = float(star.find('distance').get_text(strip=True).replace(' million km', '')) if star.find('distance') else None
    magnitude = float(star.find('absolute-magnitude').get_text(strip=True).replace(' million km', '')) if star.find('absolute-magnitude') else None


    return {
        'name': name,
        'constellation': constellation,
        'spectral': spectral,
        'radius': radius,
        'rotation': rotation,
        'age': age,
        'distance': distance,
        'magnitude': magnitude,
    }

def parse_all_files():
    data = []
    for file in os.listdir('./3'):
        if file.endswith('.xml'):
            file_path = './3/' + file
            data.append(parse_file(file_path))

    return data

def process_data(data):
    sorted_data = sorted(data, key=lambda x: x['age'] if x['age'] is not None else float(0), reverse=True)

    filtered_data = [i for i in data if i['rotation'] is not None and i['rotation'] < 365]

    distances = [i['distance'] for i in data]
    distances_stats = {
        'sum': sum(distances),
        'max': max(distances),
        'min': min(distances),
        'mean': mean(distances),
    }

    frequency_stats = Counter(i['constellation'] for i in data if i['constellation'] is not None).most_common()

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "distances_stats": distances_stats,
        "frequency_stats": frequency_stats,
    }

def save_data(sorted_data, filtered_data, distances_stats, frequency_stats):
    with open('sorted_data.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)
    with open('filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    with open('distances_stats.json', 'w', encoding='utf-8') as file:
        json.dump(distances_stats, file, ensure_ascii=False, indent=4)
    with open('frequency_stats.json', 'w', encoding='utf-8') as file:
        json.dump(frequency_stats, file, ensure_ascii=False, indent=4)

results = process_data(parse_all_files())

save_data(results['sorted_data'], results['filtered_data'], results['distances_stats'], results['frequency_stats'])