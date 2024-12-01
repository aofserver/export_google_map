import os
import json
import time
import csv
import requests
from pathlib import Path

list_file = os.listdir("output")
list_file = sorted(list_file, key=lambda x: int(x[1:-5]))


def GetToken():
    url = "https://raw.githubusercontent.com/aofserver/export_google_map/refs/heads/main/token.txt"
    response = requests.request("GET", url)
    return str(response.text.replace("\n",""))

def GetGmap(id):
    url = f"https://content-places.googleapis.com/v1/places/{id}?fields=id,name,types,nationalPhoneNumber,formattedAddress,addressComponents,viewport,rating,googleMapsUri,regularOpeningHours,userRatingCount,displayName,shortFormattedAddress,googleMapsLinks,primaryTypeDisplayName,primaryType"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': 'Bearer ' + GetToken()
    }
    response = requests.request("GET", url, headers=headers, data={})
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        print("[ERROR AUTH]")
        print(response.json())
        # send noti
        url = "https://notify-api.line.me/api/notify"
        payload = 'message=Token%20%E0%B8%AB%E0%B8%A1%E0%B8%94%E0%B8%AD%E0%B8%B2%E0%B8%A2%E0%B8%B8'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer FkVn9bJSz3OeZL4R9O189FLS7xd1sLNeUmb2XRh25r1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        time.sleep(600)
        r = GetGmap(id)
        return r


for filename in list_file:
    if Path(filename).suffix != ".json" or filename[0] != "P":
        continue
    result = []
    with open(f'output/{filename}', 'r') as file:
        print(f"read file {filename}")
        data_all = json.load(file)
    data_len = len(data_all) - 1
    for id, data in enumerate(list(data_all)):
        province_id = int(filename.replace("P","").split(".")[0])
        if province_id < int(os.getenv('province_id',"0")):
            continue
        print(f"..... {id}/{data_len}", data["id"], filename)
        r = GetGmap(data["id"])
        result.append(r)
    with open(f"output/{filename.replace('P','T')}", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
