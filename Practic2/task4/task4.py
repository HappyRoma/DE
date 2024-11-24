import pickle
import json

with open('fourth_task_products.json', 'rb') as f:
    products = pickle.load(f)
    product_dict = { product['name']: product for product in products }

with open('fourth_task_updates.json', 'r', encoding='utf-8') as f:
    updates = json.load(f)

for update in updates:
    product_name = update['name']
    method = update['method']
    param = update['param']

    if product_name in product_dict:
        if method == 'add':
            product_dict[product_name]['price'] += param
        elif method == 'sub':
            product_dict[product_name]['price'] -= param
        elif method == 'percent+':
            product_dict[product_name]['price'] += product_dict[product_name]['price'] * param
        elif method == 'percent-':
            product_dict[product_name]['price'] -= product_dict[product_name]['price'] * param

with open('fourth_task_products.json', 'wb') as f:
    pickle.dump(list(product_dict.values()), f)