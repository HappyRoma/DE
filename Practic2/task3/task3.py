import json
import msgpack
import os

with open('third_task.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

aggregated_data = {}

for product in products:
    name = product['name']
    price = product['price']

    if name not in aggregated_data:
        aggregated_data[name] = {
            'sum_price': price,
            'min_price': price,
            'max_price': price,
            'count': 1
        }
    else:
        aggregated_data[name]['sum_price'] += price
        aggregated_data[name]['min_price'] = min(aggregated_data[name]['min_price'], price)
        aggregated_data[name]['max_price'] = max(aggregated_data[name]['max_price'], price)
        aggregated_data[name]['count'] += 1

result = {
    name: {
        'average_price': data['sum_price'] / data['count'],
        'min_price': data['min_price'],
        'max_price': data['max_price']
    }
    for name, data in aggregated_data.items()
}

with open('third_task_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

with open('third_task_result.msgpack', 'wb') as f:
    msgpack.pack(result, f)

print(f"Размер файла json: {os.path.getsize('third_task_result.json')} байт")
print(f"Размер файла msgpack: {os.path.getsize('third_task_result.msgpack')} байт")