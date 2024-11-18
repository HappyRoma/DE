import pandas as pd

def rewrite_data():
    data = pd.read_html("fifth_task.html", encoding="utf-8")
    pd.DataFrame(data[0]).to_csv("fifth_task.csv", sep=',', index=False)

rewrite_data()
