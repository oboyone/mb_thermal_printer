import ijson
import time
import requests
import json


creatures = {}

# Open the JSON file from MTGJSON
with open('AtomicCards.json', 'r', encoding='utf-8') as file:
    # Parse the JSON objects one by one
    parser = ijson.items(file, 'data')
    # Iterate over the JSON card objects
    for item in parser:
        # Process each JSON object and get needed values, I chose to ignore mtg arena only cards and un cards
        try:
            for key, value in item.items():
                if "Creature" in value[0]["type"]:
                    if value[0]["legalities"] and "A-" not in value[0]["name"]:
                        creatures[key] = value       
        except:
            pass              

counter = 0 #scryfall supports 70 items in each payload
loop_counter = 0 #keep track of how many api calls we send, mostly used to see that the script is working
payload = {'identifiers':[]} #identifier payload for scryfall api calll
image_urls = []
for key, value in creatures.items():
#    print(value[0]["identifiers"]["scryfallOracleId"])
    counter = counter + 1
    payload["identifiers"].append({'oracle_id':value[0]["identifiers"]["scryfallOracleId"]})
    if counter > 70:
#        print(payload)
        time.sleep(300/1000) #scryfall has an API limit, this prevents us from hitting that 
        response = requests.post('https://api.scryfall.com/cards/collection', json=payload)
        counter = 0
        response_dict = json.loads(response.text)
        for item in response_dict["data"]: #save image urls to list 
            try:
                image_urls.append({"name":item["name"], "image_url":item["image_uris"]["large"], "cmc":item["cmc"]})
#               print(image_urls)
            except:
                pass
        response = {} #clear response json
        payload = {'identifiers':[]} #clear payload
        loop_counter = loop_counter + 1
        print(loop_counter) #how many loops have we executed

with open('creatures_image_urls.json', 'w') as fout: #write image url's to json file
    json.dump(image_urls, fout)