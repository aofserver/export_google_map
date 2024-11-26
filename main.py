import os
import json
import google_map
import summary_file
from dotenv import load_dotenv
load_dotenv()

with open('provinces-th/geographies.json', 'r') as file:
    geographies = json.load(file)
    geographies = sorted(geographies, key=lambda x: x['id'])
with open('provinces-th/provinces.json', 'r') as file:
    provinces = json.load(file)
    provinces = sorted(provinces, key=lambda x: x['id'])
with open('provinces-th/amphures.json', 'r') as file:
    amphures = json.load(file)
    amphures = sorted(amphures, key=lambda x: x['id'])
with open('provinces-th/tambons.json', 'r') as file:
    tambons = json.load(file)
    tambons = sorted(tambons, key=lambda x: x['id'])

keyword = [
    "อู่เปลี่ยนถ่ายน้ำมันเครื่องรถยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายน้ำมันเครื่องรถยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายน้ำมันเครื่องมอเตอร์ไซค์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "อู่เปลี่ยนถ่ายน้ำมันเครื่องรถยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "อู่เปลี่ยนถ่ายน้ำมันเครื่องมอเตอร์ไซค์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านซ่อมจักรยานยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายเครื่องมือและอุปกรณ์การเกษตรใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ศูนย์ซ่อมรถยนต์และรถบรรทุกใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "อู่ซ่อมรถยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายอะไหล่รถยนต์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "สถานีบริการน้ำมันใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
]
for id_k, k in enumerate(keyword):
  output_all = []
  len_filtered_provinces = len(provinces)
  for id_p, p in enumerate(provinces):
    if os.getenv('province_id'):
      if id_p > int(os.getenv('province_id')) and id_p < int(os.getenv('province_id')):
        continue
    print("...",f"{id_p+1}/{len_filtered_provinces}", p["name_th"], p["id"], id_k)
    filtered_amphures = [amphure for amphure in amphures if amphure["province_id"] == p["id"]]
    len_filtered_amphures = len(filtered_amphures)
    for id_a, a in enumerate(filtered_amphures):
      if id_a < int(os.getenv('amphure_id')):
        continue
      print(".....",f"{id_a+1}/{len_filtered_amphures}", a["name_th"], a["id"])
      filtered_tambons = [tambon for tambon in tambons if tambon["amphure_id"] == a["id"]]
      len_filtered_tambons = len(filtered_tambons)
      for id_t, t in enumerate(filtered_tambons):
        if id_t < int(os.getenv('tambon_id')):
          continue
        print("........",f"{id_t+1}/{len_filtered_tambons}", t["name_th"], t["id"])
        textQuery = k.format(province=p["name_th"], amphure=a["name_th"], tambon=t["name_th"])
        result = google_map.QueryGoogleMap(textQuery)
        for r in result:
          output_all.append(r)

      with open(f"output/K{id_k}_{p['id']}_{a['id']}.json", "w", encoding='utf-8') as f:
        json.dump(output_all, f, ensure_ascii=False, indent=4)

      summary_file.Save()
