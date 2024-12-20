# ref : https://developers.google.com/maps/documentation/places/web-service/text-search?hl=th&apix_params=%7B%22fields%22%3A%22*%22%2C%22resource%22%3A%7B%22textQuery%22%3A%22%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B8%8B%E0%B9%88%E0%B8%AD%E0%B8%A1%E0%B8%A3%E0%B8%96%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2%22%7D%7D
# ref : https://developers.google.com/maps/billing-and-pricing/pricing?hl=th#id-textsearch
# ref : https://console.cloud.google.com/apis/library/places.googleapis.com

import os
import time
import requests
import json
from dotenv import load_dotenv
load_dotenv()


def GetToken():
    url = "https://raw.githubusercontent.com/aofserver/export_google_map/refs/heads/main/token.txt"
    response = requests.request("GET", url)
    return str(response.text.replace("\n",""))


def MapAPI(textQuery, nextPageToken=""):
    api_key = os.getenv('api_key')
    # access_token = os.getenv('access_token')
    access_token = GetToken()

    url = "https://content-places.googleapis.com/v1/places:searchText?alt=json&pageSize=20"
    if bool(nextPageToken):
        url = url + f"&pageToken={nextPageToken}"

    payload = json.dumps({ "textQuery": textQuery })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    
    if access_token:
        url = url + "&fields=places.id,places.name,places.types,places.nationalPhoneNumber,places.formattedAddress,places.addressComponents,places.viewport,places.rating,places.googleMapsUri,places.regularOpeningHours,places.userRatingCount,places.displayName,places.shortFormattedAddress,places.googleMapsLinks,places.primaryTypeDisplayName,places.primaryType,nextPageToken,searchUri"
        headers["authorization"] = 'Bearer ' + access_token
    elif api_key:
        headers["X-Goog-Api-Key"] = api_key
        headers["X-Goog-FieldMask"] = 'places.id,places.name,places.types,places.nationalPhoneNumber,places.formattedAddress,places.addressComponents,places.viewport,places.rating,places.googleMapsUri,places.regularOpeningHours,places.userRatingCount,places.displayName,places.shortFormattedAddress,places.googleMapsLinks,places.primaryTypeDisplayName,places.primaryType,nextPageToken,searchUri'

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        response = response.json()
        return response.get("places"), response.get("nextPageToken")
    else:
        print("[ERROR AUTH]")
        # send noti
        url = "https://notify-api.line.me/api/notify"
        payload = 'message=Token%20%E0%B8%AB%E0%B8%A1%E0%B8%94%E0%B8%AD%E0%B8%B2%E0%B8%A2%E0%B8%B8'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer FkVn9bJSz3OeZL4R9O189FLS7xd1sLNeUmb2XRh25r1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        time.sleep(600)
        p, n = MapAPI(textQuery, nextPageToken)
        return p, n

def QueryGoogleMap(textQuery):
    result = []
    nextPageToken = ""
    while True:
        places, nextPageToken = MapAPI(textQuery, nextPageToken)
        if not bool(places):
          break
        for p in places:
            if p.get("reviews"):
                del p["reviews"]
            if p.get("photos"):
                del p["photos"]
            if p.get("addressDescriptor"):
                del p["addressDescriptor"]
        result.extend(places)
        if nextPageToken is None:
            break
    return result