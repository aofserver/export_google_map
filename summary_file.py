import os
import json
import csv
from pathlib import Path

def Save(folder="output",summary_filename="data"):
    # find data not duplicate 
    result = []
    province_id = int(summary_filename.replace("P",""))
    path = f'{folder}/{summary_filename}.json'
    if os.path.isfile(path):
        with open(path, 'r') as file:
            result = json.load(file)

    list_file = os.listdir(folder)
    for filename in list_file:
        if Path(filename).suffix != ".json" or filename[0] == "P" or filename[0] != "K":
            continue
        if int(filename.split("_")[1]) == province_id:
            with open(f'{folder}/{filename}', 'r') as file:
                data_all = json.load(file)
            for data in list(data_all):
                check = [r for r in result if r["id"] == data["id"]]
                if not check:
                    result.append(data)
            if Path(filename).suffix == ".json" and filename != f"{summary_filename}.json":
                os.remove(f'{folder}/{filename}')

    # write json file
    with open(f"{folder}/{summary_filename}.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


# Save(folder="output",summary_filename="P0")