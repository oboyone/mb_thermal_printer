import ijson
import time
import requests
import json
import urllib.request 
import ast

with open('creatures_image_urls.json', 'r', encoding='utf-8') as file: #open creature url json
    # Parse the JSON objects one by one
    parser = ast.literal_eval(file.read())
    for item in parser:
        url = item["image_url"]
        cmc = int(item["cmc"])
        name = item["name"]
        save_path = str(str(cmc) + '/' + name.replace("'", "").replace('"', "").replace("/","")  + ".jpg") #creates a folder per cmc and fills it with the images 
        urllib.request.urlretrieve(url, save_path) 
        # Process each JSON object as needed
