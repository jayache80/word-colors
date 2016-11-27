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
from math import sqrt

try:
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request,urlopen

load_dotenv(find_dotenv())
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CX = os.environ.get("CX")

query_string = "dog"

request_url = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_API_KEY + "&cx=" + CX + "&searchType=image" + "&q=" + query_string
response = requests.get(request_url)
j = response.json()
items = j["items"]
print("================== items are: ==================")
for item in items:
    print(item["link"])
count = 0
results_set = []
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

        for result in results:
            print(kmeans.rgb_to_hex(result))
            results_set.append(result)
            print("image", count, "has color:", result)

    except:
        print("Unexpected error:", sys.exc_info()[0])
    
    count = count + 1

delta_thresh = 20

for i in range(len(results_set) - 1):
    # print("i is", i)
    
    for j in range(len(results_set) - 1 - i):
        k = len(results_set ) - 1 - j

        r1 = results_set[i][0]
        r2 = results_set[k][0]

        g1 = results_set[i][1]
        g2 = results_set[k][1]

        b1 = results_set[i][2]
        b2 = results_set[k][2]

        delta = sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
        if delta <= delta_thresh:
            print("results", i, results_set[i], "and", k, results_set[k], "are similar!")


# print(json.dumps(j, sort_keys=True, indent=4))
