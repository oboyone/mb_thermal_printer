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
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

counter = 0 #scryfall supports 70 items in each payload
payload_counter = 0 #keep track of how many api calls we send, mostly used to see that the script is working
payload = {'identifiers':[]} #identifier payload for scryfall api calll
creature_count = len(creatures)
estimated_payloads = int(creature_count/70) + (creature_count % 70 > 0)
image_urls = []
for index, (key, value) in enumerate(creatures.items()):
    counter += 1
    payload["identifiers"].append({'oracle_id':value[0]["identifiers"]["scryfallOracleId"]})
    if counter > 70 or index == creature_count - 1:
        time.sleep(0.3) 
        response = requests.post('https://api.scryfall.com/cards/collection', json=payload)
        counter = 0
        try:
            response.raise_for_status()
            response_dict = response.json()
            for item in response_dict["data"]: #save image urls to list 
                try:
                    image_urls.append({"name":item["name"], "image_url":item["image_uris"]["large"], "cmc":item["cmc"]})
                except Exception as e:
                    print(f"An error occurred while processing response data: {e}")
                    continue
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            continue
        finally:
            response = {} #clear response json
            payload = {'identifiers':[]} #clear payload
            payload_counter += 1
            print(f"Payload number {payload_counter}, out of {estimated_payloads}") #how many payloads we have sent

with open('creatures_image_urls.json', 'w') as fout: #write image url's to json file
    json.dump(image_urls, fout)
