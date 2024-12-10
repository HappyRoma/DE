import sqlite3

import pandas as pd

# data = pd.DataFrame(pd.read_csv('./data/_part_2.csv', delimiter=';'))
# print(data.head())
# data2 = pd.DataFrame(pd.read_pickle('./data/_part_1.pkl'))
# print()
# dup = data2['song'].duplicated(keep=False)
# print(data2.head())

def create_db(connection):
    data1 = pd.DataFrame(pd.read_pickle('./data/_part_1.pkl'))
    data2 = pd.DataFrame(pd.read_csv('./data/_part_2.csv', delimiter=';'))

    all_columns = ['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre',
                   'acousticness',
                   'energy',
                   'popularity',
                   'key',
                   'loudness']
    data1 = data1.reindex(columns=all_columns, fill_value=None)
    data2 = data2.reindex(columns=all_columns, fill_value=None)


    merged = pd.concat([data1, data2], ignore_index=True)


    cursor = connection.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS music (
       artist TEXT,
       song TEXT,
       duration_ms INTEGER,
       year INTEGER,
       tempo REAL,
       genre TEXT,
       acousticness REAL,
       energy REAL,
       popularity INTEGER,
       key INTEGER,
       loudness REAL,
       UNIQUE (artist, song, duration_ms)
    )
    ''')

    for x, row in merged.iterrows():
        cursor.execute('''
            INSERT INTO music (
                artist, song, duration_ms, year, tempo, genre,
                acousticness, energy, popularity, key, loudness
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artist, song, duration_ms)
            DO UPDATE SET
                year = COALESCE(EXCLUDED.year, music.year),
                tempo = COALESCE(EXCLUDED.tempo, music.tempo),
                genre = COALESCE(EXCLUDED.genre, music.genre),
                acousticness = COALESCE(EXCLUDED.acousticness, music.acousticness),
                energy = COALESCE(EXCLUDED.energy, music.energy),
                popularity = COALESCE(EXCLUDED.popularity, music.popularity),
                key = COALESCE(EXCLUDED.key, music.key),
                loudness = COALESCE(EXCLUDED.loudness, music.loudness)
        ''', tuple(row[col] for col in all_columns))

    connection.commit()


def db_analyse(connection):
    # Вывод первых 86, отсортированных по popularity
    query_1 = '''
        SELECT * from music
        WHERE popularity IS NOT NULL
        ORDER BY popularity DESC
        LIMIT 86
        '''

    result_1 = pd.read_sql_query(query_1, connection)
    result_1.to_json('result1.json', force_ascii=False, orient='records', indent=4)

    # Вывод статистики по energy
    query_2 = '''
        SELECT 
        SUM(energy) AS energy_sum,
        MIN(energy) AS energy_min,
        MAX(energy) AS energy_max,
        AVG(energy) AS energy_avg
        FROM music
        '''

    result_2 = pd.read_sql_query(query_2, connection)
    result_2.to_json('result2.json', force_ascii=False, orient='records', indent=4)

    # Вывод частоты artist
    query_3 = '''
        SELECT artist, COUNT(*) as count FROM music
        GROUP BY artist
        ORDER BY count DESC
        '''

    result_3 = pd.read_sql_query(query_3, connection)
    result_3.to_json('result3.json', force_ascii=False, orient='records', indent=4)

    # отфильтрованный вывод по duration_ms > 200000
    query_4 = '''
        SELECT * from music
        WHERE duration_ms > 200000
        ORDER BY tempo DESC 
        LIMIT 91
        '''

    result_4 = pd.read_sql_query(query_4, connection)
    result_4.to_json('result4.json', force_ascii=False, orient='records', indent=4)

    connection.commit()


connect = sqlite3.connect('./../data-1-2/database.db')
create_db(connect)
db_analyse(connect)
connect.close()
