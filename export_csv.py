import os
import json
import csv
from pathlib import Path

# find data not duplicate 
result = []
list_file = os.listdir("output")
for filename in list_file:
    if Path(filename).suffix != ".json":
        continue
    with open(f'output/{filename}', 'r') as file:
        print(f"read file {filename}")
        data_all = json.load(file)
    for data in list(data_all):
        check = [r for r in result if r["id"] == data["id"]]
        if not check:
            result.append(data)


def FindAddress(textFind, addressComponents):
    for a in addressComponents:
        if type(textFind) == str:
            check =  [t for t in a["types"] if t == textFind]
        elif type(textFind) == list:
            for text in textFind:
                check = [t for t in a["types"] if t == text]
                if check:
                    return a["longText"]
        if check:
            return a["longText"]
    return ""


# prepare data
excel_data = []
for r in result:
    latitude = r.get("viewport").get("high").get("latitude") if r.get("viewport") else ""
    longitude = r.get("viewport").get("high").get("longitude") if r.get("viewport") else ""
    displayName = r.get("displayName").get("text") if r.get("displayName") else ""
    primaryTypeDisplayName = r.get("primaryTypeDisplayName").get("text") if r.get("primaryTypeDisplayName") else ""
    if r.get("regularOpeningHours"):
        if r["regularOpeningHours"]["periods"][0].get("close"):
            openTime = f'{r["regularOpeningHours"]["periods"][0]["open"]["hour"]}:{r["regularOpeningHours"]["periods"][0]["open"]["minute"]}' if r["regularOpeningHours"] else ""
            closeTime = f'{r["regularOpeningHours"]["periods"][0]["close"]["hour"]}:{r["regularOpeningHours"]["periods"][0]["close"]["minute"]}' if r["regularOpeningHours"] else ""
        else:
            openTime = "เปิด 24 ชั่วโมง"
            closeTime = "เปิด 24 ชั่วโมง"
    else:
        openTime = ""
        closeTime = ""
    addressSubdistrict = FindAddress(["locality","sublocality_level_1"],r.get("addressComponents"))
    addressDistrict = FindAddress(["administrative_area_level_2"],r.get("addressComponents"))
    addressProvince = FindAddress(["administrative_area_level_1"],r.get("addressComponents"))
    addressCountry = FindAddress("country",r.get("addressComponents"))
    addressZipcode = FindAddress("postal_code",r.get("addressComponents"))

    if addressSubdistrict:
        addressDetail = r.get("formattedAddress").split(addressSubdistrict)[0].strip()
    elif addressDistrict:
        addressDetail = r.get("formattedAddress").split(addressDistrict)[0].strip()
    else:
        addressDetail = ""
    
    data = {
        "id": r.get("id"),
        "ชื่อร้าน": displayName,
        "เบอร์โทร": r.get("nationalPhoneNumber"),
        "คะแนน": r.get("rating"),
        "จำนวนคนที่ให้คะแนน": r.get("userRatingCount"),
        "googleMaps": r.get("googleMapsUri"),
        "ประเภท": ", ".join(r.get("types")),
        "ประเภทหลัก": r.get("primaryType"),
        "ชื่อประเภทหลัก": primaryTypeDisplayName,
        "เวลเปิด": openTime,
        "เวลปิด": closeTime,
        "latitude": latitude,
        "longitude": longitude,
        "ที่อยู่เต็ม": r.get("formattedAddress"),
        "ที่อยู่": addressDetail,
        "ตำบล": addressSubdistrict,
        "อำเภอ": addressDistrict,
        "จังหวัด": addressProvince,
        "ประเทศ": addressCountry,
        "รหัสไปรษณี": addressZipcode,
    }

    excel_data.append(data)

# write file csv
data_file = open('data.csv', 'w')
csv_writer = csv.writer(data_file)
count = 0
for data in excel_data:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
data_file.close()


# write json file
with open(f"data.json", "w", encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)