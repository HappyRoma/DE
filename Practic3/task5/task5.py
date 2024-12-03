import json
import re
import requests
from bs4 import BeautifulSoup
import time
from collections import Counter
from statistics import mean

katalog_url = 'https://www.realtor.com/realestateandhomes-search/Madison_WI/show-recently-sold/sby-6'

pages_urls = [
    'https://www.realtor.com/realestateandhomes-detail/910-Tramore-Trl_Madison_WI_53717_M77304-35529',
    'https://www.realtor.com/realestateandhomes-detail/1910-E-Washington-Ave_Madison_WI_53704_M73297-07693',
    'https://www.realtor.com/realestateandhomes-detail/155-E-Wilson-St-Apt-204_Madison_WI_53703_M84257-08847',
    'https://www.realtor.com/realestateandhomes-detail/1142-E-Mifflin-St_Madison_WI_53703_M77463-50715',
    'https://www.realtor.com/realestateandhomes-detail/4817-Poplar-Creek-Dr_Madison_WI_53718_M70052-57957',
    'https://www.realtor.com/realestateandhomes-detail/29-Belmont-Rd_Madison_WI_53714_M75984-97125',
    'https://www.realtor.com/realestateandhomes-detail/4513-Goldfinch-Dr_Madison_WI_53714_M83631-89894',
    'https://www.realtor.com/realestateandhomes-detail/6-Quinn-Cir_Madison_WI_53713_M88365-41895',
    'https://www.realtor.com/realestateandhomes-detail/5433-Greening-Ln_Madison_WI_53705_M81230-59533',
    'https://www.realtor.com/realestateandhomes-detail/2322-Upham-St_Madison_WI_53704_M73090-60773',
    'https://www.realtor.com/realestateandhomes-detail/5453-Congress-Ave_Madison_WI_53718_M74480-08046',
    'https://www.realtor.com/realestateandhomes-detail/625-E-Gorham-St_Madison_WI_53703_M72469-16222',
    'https://www.realtor.com/realestateandhomes-detail/3214-Clove-Dr_Madison_WI_53704_M85176-84861',
    'https://www.realtor.com/realestateandhomes-detail/325-E-Dean-Ave_Madison_WI_53716_M86762-61076'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/538.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def parse_katalog():
    with open('./html.html', 'r', encoding='utf-8') as f:
        data = BeautifulSoup(f, 'html.parser')

    property_items = []
    # Класс используется не только в объектах каталога, а в каких-то скрытых элементах, поэтому фильтруем
    property_list = [element for element in data.find_all('div', class_='card-content') if element.find('a')]

    for property in property_list:
        sold_date = property.find('div', class_='StatusBadgestyles__StyledStatusBadge-rui__sc-1wog16p-0').find('div').get_text(strip=True).replace('Sold - ', '')
        price = property.find('span', class_='base__StyledType-rui__sc-108xfm0-0').get_text(strip=True).replace('$', '').replace(',', '')
        beds = int(property.find('li', class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0').find('span').get_text(strip=True).split(' ')[0]) if property.find('li', class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0').find('span').get_text(strip=True).isdigit() else 0
        baths = float(property.find('li', class_='PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0').find('span').get_text(strip=True).replace('+', '').split(' ')[0])
        sqft = float(re.sub('[^0-9]','', property.find('li', class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0').find('span').find('span').get_text(strip=True).split(' ')[0])) if property.find('li', class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0') else None
        sqft_lot = float(re.sub('[^0-9]','', property.find('li', class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0').find('span').find('span').get_text(strip=True))) if property.find('li', class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0') else None
        code = property.find('div', class_='card-address').find_all('div')[-1].get_text(strip=True).split(', ')[-1] if property.find('div', class_='card-address') else None

        property_items.append({
            'sold_date': sold_date,
            'price': price,
            'beds': beds,
            'baths': baths,
            'sqft': sqft,
            'sqft_lot': sqft_lot,
            'code': code,
        })

    return property_items

def parse_detail(data):

    property = data.find('div', class_='iQuhWL')


    price = int(property.find('h2', class_='base__StyledType-rui__sc-108xfm0-0').get_text(strip=True).replace('$', '').replace(',', ''))
    beds = int(property.find('li', class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0').find('span').get_text(strip=True).split(' ')[0]) if property.find('li', class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0').find('span').get_text(strip=True).isdigit() else 0
    baths = float(property.find('li', class_='PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0').find('span').get_text(strip=True).replace('+', '').split(' ')[0])
    sqft = float(re.sub('[^0-9]','', property.find('li', class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0').find('span').find('span').get_text(strip=True))) if property.find('li', class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0') else None
    sqft_lot = float(re.sub('[^0-9]','', property.find('li', class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0').find('span').find('span').get_text(strip=True))) if property.find('li', class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0') else None
    year = int(property.find('ul', {'data-testid': 'key-facts'}).find_all('li')[1].find('p').get_text(strip=True))
    type = property.find('ul', {'data-testid': 'key-facts'}).find_all('li')[0].find('p').get_text(strip=True)
    garage_capacity = int(property.find('ul', {'data-testid': 'key-facts'}).find_all('li')[4].find('p').get_text(strip=True).replace(' Car', '')) if len(property.find('ul', {'data-testid': 'key-facts'}).find_all('li')) > 4 else None

    return [{
        'price': price,
        'beds': beds,
        'baths': baths,
        'sqft': sqft,
        'sqft_lot': sqft_lot,
        'year': year,
        'type': type,
        'garage_capacity': garage_capacity,
    }]


def parse_detail_all_pages():
    data_list = []

    for page in pages_urls:
        request = requests.get(page, headers=headers)
        data = BeautifulSoup(request.content, 'html.parser')
        # Кидаем цикл в слип, чтобы не нарваться на защиту от ботов
        time.sleep(2)
        data_list.extend(parse_detail(data))

    return data_list

def process_data_katalog(data):
    sorted_data = sorted(data, key=lambda x: x['price'] if x['price'] is not None else 0, reverse=True)

    filtered_data = [i for i in data if i['beds'] is not None and i['beds'] > 2]

    sqft = [i['sqft'] for i in data if i['sqft'] is not None]
    sqft_stats = {
        'sum': sum(sqft),
        'max': max(sqft),
        'min': min(sqft),
        'mean': mean(sqft),
    }

    frequency_stats = Counter(i['code'] for i in data if i['code'] is not None).most_common()

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "sqft_stats": sqft_stats,
        "frequency_stats": frequency_stats,
    }

def process_data_detail(data):
    sorted_data = sorted(data, key=lambda x: x['price'] if x['price'] is not None else 0, reverse=True)

    filtered_data = [i for i in data if i['year'] is not None and i['year'] > 2000]

    garage_capacity = [i['garage_capacity'] for i in data if i['garage_capacity'] is not None]
    garage_capacity_stats = {
        'sum': sum(garage_capacity),
        'max': max(garage_capacity),
        'min': min(garage_capacity),
        'mean': mean(garage_capacity),
    }

    frequency_stats = Counter(i['type'] for i in data if i['type'] is not None).most_common()

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "garage_capacity": garage_capacity_stats,
        "frequency_stats": frequency_stats,
    }

def save_data(sorted_data, filtered_data, stats, frequency_stats, filename):
    with open(f'{filename}_sorted_data.json', 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)
    with open(f'{filename}_filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    with open(f'{filename}_stats.json', 'w', encoding='utf-8') as file:
        json.dump(stats, file, ensure_ascii=False, indent=4)
    with open(f'{filename}_frequency_stats.json', 'w', encoding='utf-8') as file:
        json.dump(frequency_stats, file, ensure_ascii=False, indent=4)

katalog_results = process_data_katalog(parse_katalog())
save_data(katalog_results['sorted_data'], katalog_results['filtered_data'], katalog_results['sqft_stats'], katalog_results['frequency_stats'], 'katalog')

detail_results = process_data_detail(parse_detail_all_pages())
save_data(detail_results['sorted_data'], detail_results['filtered_data'], detail_results['garage_capacity'], detail_results['frequency_stats'], 'detail')
