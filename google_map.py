# ref : https://developers.google.com/maps/documentation/places/web-service/text-search?hl=th&apix_params=%7B%22fields%22%3A%22*%22%2C%22resource%22%3A%7B%22textQuery%22%3A%22%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B8%8B%E0%B9%88%E0%B8%AD%E0%B8%A1%E0%B8%A3%E0%B8%96%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2%22%7D%7D
# ref : https://developers.google.com/maps/billing-and-pricing/pricing?hl=th#id-textsearch

import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')

def GetToken():
    url = ""
    response = requests.request("GET", url)




def MapAPI(textQuery, nextPageToken=""):
    global token
    url = "https://content-places.googleapis.com/v1/places:searchText?fields=*&alt=json&pageSize=20"
    if bool(nextPageToken):
        url = url + f"&pageToken={nextPageToken}"

    payload = json.dumps({
        "textQuery": textQuery
    })
    headers = {
        'accept': '*/*',
        'accept-language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json',
        'origin': 'https://content-places.googleapis.com',
        'priority': 'u=1, i',
        'referer': 'https://content-places.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.lb.th.44uDDJ66DBs.O%2Fam%3DAACA%2Fd%3D1%2Frs%3DAHpOoo_1t22RprkAiUJsA6uts_cGae0afg%2Fm%3D__features__',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-client-data': 'CKO1yQEIk7bJAQimtskBCKmdygEIt5LLAQiWocsBCIagzQEIusjNAQjVrM4BCPq+zgEIo8TOAQiTxs4BCJfLzgEIw8zOAQjGzM4BGPXJzQEYnbHOARj/yc4B',
        'x-clientdetails': 'appVersion=5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F130.0.0.0%20Safari%2F537.36&platform=MacIntel&userAgent=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F130.0.0.0%20Safari%2F537.36',
        'x-goog-encode-response-if-executable': 'base64',
        'x-javascript-user-agent': 'apix/3.0.0 google-api-javascript-client/1.1.0',
        'x-origin': 'https://explorer.apis.google.com',
        'x-referer': 'https://explorer.apis.google.com',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
      response = response.json()
      return response.get("places"), response.get("nextPageToken")
    else:
      print("[ERROR AUTH]")

def QueryGoogleMap(textQuery):
    result = []
    nextPageToken = ""
    while True:
        places, nextPageToken = MapAPI(textQuery, nextPageToken)
        if not bool(places):
          break
        result.extend(places)
        if nextPageToken is None:
            break
    return result