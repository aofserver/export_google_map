import os
import json
import csv
from pathlib import Path


def Save():
    # find data not duplicate 
    result = []
    path = 'output/data.json'
    if os.path.isfile(path):
        with open(path, 'r') as file:
            result = json.load(file)

    list_file = os.listdir("output")
    for filename in list_file:
        if Path(filename).suffix != ".json" and filename != "data.json":
            continue
        with open(f'output/{filename}', 'r') as file:
            data_all = json.load(file)
        for data in list(data_all):
            check = [r for r in result if r["id"] == data["id"]]
            if not check:
                result.append(data)
        print(f'Remove output/{filename}')
        os.remove(f'output/{filename}')

    # write json file
    with open(f"output/data.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)