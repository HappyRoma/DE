import sqlite3

import pandas as pd

def create_db(connection):
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        price REAL,
        quantity INTEGER,
        fromCity TEXT,
        isAvailable BOOLEAN,
        views INTEGER,
        category TEXT,
        update_count INTEGER DEFAULT 0
    )
    ''')

    data = pd.DataFrame(pd.read_pickle('./_product_data.pkl'))

    prepared_data = data[data.columns].values.tolist()

    cursor.executemany('''
    INSERT OR IGNORE INTO products (name, price, quantity, fromCity, isAvailable, views, category)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', prepared_data)

    connection.commit()

def load_update_file():
    with open('./_update_data.text', 'r') as f:
        updates = f.read()

        return updates

def process_updates(connection, name, method, param):
    cursor = connection.cursor()

    if method == 'price_percent':
        cursor.execute('UPDATE products SET price = price * (1 + ?) WHERE name = ? AND price >= 0', (float(param), name))
    elif method == 'price_abs':
        cursor.execute('UPDATE products SET price = price + ? WHERE name = ? AND price + ? >= 0', (float(param), name, float(param)))
    elif method == 'quantity_sub':
        cursor.execute('UPDATE products SET quantity = quantity + ? WHERE name = ? AND quantity + ? >= 0', (int(param), name, int(param)))
    elif method == 'quantity_add':
        cursor.execute('UPDATE products SET quantity = quantity + ? WHERE name = ?', (int(param), name))
    elif method == 'available':
        cursor.execute('UPDATE products SET isAvailable  = ? WHERE name = ?', (param.lower() == 'true', name))
    elif method == 'remove':
        cursor.execute('DELETE FROM products WHERE name = ?', (name,))

    cursor.execute('UPDATE products SET update_count = update_count + 1 WHERE name = ?', (name,))
    cursor.execute('COMMIT')

def update_db(connection):
    for update in load_update_file().split('====='):
        if update:
            lines = update.strip().split('\n')
            name = lines[0].split('::')[1]
            method = lines[1].split(':')[1]
            param = lines[2].split(':')[1] if len(lines) > 2 else None
            process_updates(connection, name, method, param)

def analyse_db(connection):

    query_1 = '''
    SELECT * from products
    ORDER BY update_count DESC
    LIMIT 10
    '''

    result_1 = pd.read_sql_query(query_1, connection)
    print('Топ-10 Самых обновляемых товаров:')
    print(result_1)

    query_2 = '''
        SELECT category,
        SUM(price) AS sum_price,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS avg_price,
        COUNT(*) AS count
        FROM products
        GROUP BY category
        '''

    result_2 = pd.read_sql_query(query_2, connection)
    print('Анализ цен на товары по группам:')
    print(result_2)

    query_3 = '''
         SELECT category,
         SUM(quantity) AS quantity_sum,
         MIN(quantity) AS quantity_min,
         MAX(quantity) AS quantity_max,
         AVG(quantity) AS quantity_avg,
         COUNT(*) AS count
         FROM products
         GROUP BY category
         '''

    result_3 = pd.read_sql_query(query_3, connection)
    print('Анализ остатков на товары по группам:')
    print(result_3)

    query_4 = '''
         SELECT category, name, MAX(views) AS max_views
         FROM products
         GROUP BY category
         ORDER BY max_views DESC
         '''

    result_4 = pd.read_sql_query(query_4, connection)
    print('Товары с наибольшим количеством просмотров в каждой категории')
    print(result_4)




connect = sqlite3.connect('./../data-1-2/database.db')
create_db(connect)
update_db(connect)
analyse_db(connect)
connect.close()