import json
import google_map

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

output_data = []
output_all = []
keyword = [
    "ร้านซ่อมรถใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายอะไหล่ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านขายน้ำมันเครื่องใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "อู่ซ่อมรถใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    "ร้านซ่อมมอไซค์ใน จังหวัด{province} อำเภอ{amphure} ตำบล{tambon}",
    ]
for id_k, k in enumerate(keyword):
  len_filtered_provinces = len(provinces)
  for id_p, p in enumerate(provinces):
    print("...",f"{id_p+1}/{len_filtered_provinces}", p["name_th"], p["id"])
    filtered_amphures = [amphure for amphure in amphures if amphure["province_id"] == p["id"]]
    len_filtered_amphures = len(filtered_amphures)
    for id_a, a in enumerate(filtered_amphures):
      print(".....",f"{id_a+1}/{len_filtered_amphures}", a["name_th"], a["id"])
      filtered_tambons = [tambon for tambon in tambons if tambon["amphure_id"] == a["id"]]
      len_filtered_tambons = len(filtered_tambons)
      for id_t, t in enumerate(filtered_tambons):
        print("........",f"{id_t+1}/{len_filtered_tambons}", t["name_th"], t["id"])
        textQuery = k.format(province=p["name_th"], amphure=a["name_th"], tambon=t["name_th"])
        result = google_map.QueryGoogleMap(textQuery)
        for r in result:
          output_all.append(r)

      with open(f"output/{p['id']}_{a['id']}.json", "w", encoding='utf-8') as f:
        json.dump(output_all, f, ensure_ascii=False, indent=4)
