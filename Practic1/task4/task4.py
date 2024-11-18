import csv
import pandas as pd


def read_csv_file():
    reader = pd.read_csv("fourth_task.txt")

    return reader

def rewrite_source_file(data):
    # Возможно надо было записывать в другой файл...
    # data.drop("rating", axis=1, inplace=True)
    pd.DataFrame(data).to_csv("fourth_task.txt", sep=",", index=False)

def avg_price(data):
    return data["price"].mean()

def find_min_max_quantity(data):
    return data["quantity"].min(), data["quantity"].max()

def write_results(data):
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"2. Среднее арифметическое по столбцу price: {avg_price(data)}\n")
        file.write(f"3. Максимум по столбцу quantity: {find_min_max_quantity(data)[1]}\n")
        file.write(f"4. Минимум по столбцу quantity: {find_min_max_quantity(data)[0]}\n")

def write_filtered_table(data):
    filtered_data = data[data["quantity"] > 579]
    pd.DataFrame(filtered_data).to_csv("filtered_result.csv", sep=",", index=False)

rewrite_source_file(read_csv_file())

write_results(read_csv_file())

write_filtered_table(read_csv_file())

