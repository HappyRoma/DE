import sqlite3
import msgpack
import pandas as pd


def create_db():
    with open('./../data-1-2/subitem.msgpack', 'rb') as f:
        data = pd.DataFrame(msgpack.load(f))

    connection = sqlite3.connect('./../data-1-2/database.db')
    cursor = connection.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS book_price (
       id INTEGER PRIMARY KEY,
       title TEXT UNIQUE,
       price INTEGER,
       place TEXT,
       date DATETIME
    )
    ''')

    prepared_data = data[['title', 'price', 'place', 'date']].values.tolist()

    cursor.executemany('''
    INSERT OR IGNORE INTO book_price (title, price, place, date)
    VALUES (?, ?, ?, ?)
    ''', prepared_data)

    connection.commit()

    return connection



def db_analyse(connection):

    # Вывод первых 86, отсортированных по цене
    query_1 = '''
    SELECT * from book_price
    ORDER BY price DESC
    LIMIT 86
    '''

    result_1 = pd.read_sql_query(query_1, connection)
    result_1.to_json('result1.json', force_ascii=False, orient='records', indent=4)


    # Вывод статистики по цене
    query_2 = '''
    SELECT 
    SUM(price) AS price_sum,
    MIN(price) AS price_min,
    MAX(price) AS price_max,
    AVG(price) AS price_avg
    FROM book_price
    '''

    result_2 = pd.read_sql_query(query_2, connection)
    result_2.to_json('result2.json', force_ascii=False,  orient='records', indent=4)


    # Вывод частоты place
    query_3 = '''
    SELECT place, COUNT(*) as count FROM book_price
    GROUP BY place
    ORDER BY count DESC
    '''

    result_3 = pd.read_sql_query(query_3, connection)
    result_3.to_json('result3.json', force_ascii=False,  orient='records', indent=4)


    # отфильтрованный вывод по цене,
    query_4 = '''
    SELECT * from book_price
    WHERE price >= 1000 AND price <= 3000
    ORDER BY price DESC
    LIMIT 86
    '''

    result_4 = pd.read_sql_query(query_4, connection)
    result_4.to_json('result4.json', force_ascii=False,  orient='records', indent=4)

    connection.commit()

connect = create_db()
db_analyse(connect)
connect.close()
