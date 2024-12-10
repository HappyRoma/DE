import sqlite3
import pandas as pd

def create_db():

    data = pd.DataFrame(pd.read_pickle('./../data-1-2/item.pkl'))

    connection = sqlite3.connect('./../data-1-2/database.db')
    cursor = connection.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS book_properties (
       id INTEGER PRIMARY KEY,
       title TEXT UNIQUE,
       author TEXT,
       genre TEXT,
       pages INTEGER,
       published_year DATETIME,
       isbn TEXT,
       rating REAL,
       views INTEGER,
       FOREIGN KEY(title) REFERENCES book_price(title)
    )
    ''')

    prepared_data = data[['title', 'author', 'genre', 'pages', 'published_year', 'isbn', 'rating', 'views']].values.tolist()

    cursor.executemany('''
        INSERT OR IGNORE INTO book_properties (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', prepared_data)

    connection.commit()

    return connection

def db_analyse(connection):

    query_1 = '''
    SELECT bp.title, bpp.author, bpp.genre, bp.price, bpp.rating
    FROM book_price bp
    JOIN book_properties bpp ON bp.title = bpp.title
    WHERE bp.price < 3000
    AND bpp.rating > 4.0
    ORDER BY bp.price DESC
    LIMIT 10
    '''

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    result1 = pd.read_sql_query(query_1, connection)
    print('Книги с рейтингом больше 4.0 и дешевле 3000:')
    print(result1)

    query_2 = '''
    SELECT bpp.genre, COUNT(bp.id) as book_count
    FROM book_price bp
    JOIN book_properties bpp ON bp.title = bpp.title
    GROUP BY bpp.genre
    ORDER BY book_count DESC
    '''

    result2 = pd.read_sql_query(query_2, connection)
    print('Количество книг по жанрам:')
    print(result2)

    query_3 = '''
    SELECT bp.title, bpp.pages, bpp.rating, bpp.views
    FROM book_price bp
    JOIN book_properties bpp ON bp.title = bpp.title
    WHERE bpp.pages > 200
    AND bpp.views > 50000
    AND bpp.rating > (SELECT AVG(rating) FROM book_properties)
    ORDER BY bpp.rating DESC, bpp.pages ASC
    '''

    result3 = pd.read_sql_query(query_3, connection)
    print('Книги с более чем 200 страницами, 50000 просмотрами и рейтингом выше среднего')
    print(result3)


connect = create_db()
db_analyse(connect)
connect.close()

