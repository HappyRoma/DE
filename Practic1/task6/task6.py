import pandas as pd
import requests

def read_json():
    data = requests.get("https://jsonplaceholder.typicode.com/posts")
    pd.DataFrame(data.json()).to_html("result.html", index=False, encoding="utf-8")

read_json()
