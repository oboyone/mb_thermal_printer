import os
import urllib.request 
import json

def download_images_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            download_image(item)

def download_image(item):
    url = item["image_url"]
    cmc = int(item["cmc"])
    name = item["name"]
    
    # Create directory if it doesn't exist
    directory = str(cmc)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Construct save path, replacing special characters
    save_path = os.path.join(directory, name.replace("'", "").replace('"', "").replace("/", "") + ".jpg")
    
    try:
        urllib.request.urlretrieve(url, save_path) 
        print(f"Downloaded {name} to {save_path}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")

# Usage
download_images_from_json('creatures_image_urls.json')
