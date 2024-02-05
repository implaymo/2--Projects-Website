import requests
import json


response = requests.get("https://api.imgflip.com/get_memes")
response.raise_for_status()

data = response.json()

all_memes = []
for i in data["data"]["memes"]:
    all_memes.append(i["url"])

