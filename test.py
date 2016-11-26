#!/usr/bin/env python
import os
import json
from dotenv import load_dotenv, find_dotenv
import requests
from PIL import Image
# import urllib.request
from io import BytesIO
import sys
import kmeans

from urllib.request import Request, urlopen

load_dotenv(find_dotenv())
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CX = os.environ.get("CX")

query_string = "bird"

request_url = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_API_KEY + "&cx=" + CX + "&searchType=image" + "&q=" + query_string
response = requests.get(request_url)
j = response.json()
items = j["items"]
print("================== items are: ==================")
for item in items:
    print(item["link"])
count = 0
for item in items:
    image_string = ""
    image_url = item["link"]
    try:
        # with urllib.request.urlopen(image_url) as url:
        req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        image_string = urlopen(req).read()
        image_file = BytesIO(image_string)
        img = Image.open(image_file)
        filename = "%s.%s" %  (count, img.format)
        img.save(filename)

        k = kmeans.Kmeans()
        results = k.run(img)
        print("Results are:")
        print(results)
        k.saveCentroidColours(str(count), img.format)
        # k.showCentroidColours()
        for result in results:
            print(kmeans.rgb_to_hex(result))


    except:
        print("Unexpected error:", sys.exc_info()[0])
    
    count = count + 1

# print(json.dumps(j, sort_keys=True, indent=4))
