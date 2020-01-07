#!/usr/bin/env python3

import csv
import requests
import shelve

API_KEY = "" # request at https://api.goclimateneutral.org/api_keys

cache = shelve.open("co2-cache")

orig = csv.DictReader(open("co2.csv", "r"))
fixed = csv.DictWriter(open("co2-real.csv", "w"), orig.fieldnames)
fixed.writeheader()

for line in orig:
    key = "-".join([line[x] for x in ["src", "dst", "class_exact"]])
    if key not in cache:
        req = {
            "segments[0][origin]": line["src"],
            "segments[0][destination]": line["dst"],
            "cabin_class": line["class_exact"],
            "currencies[]": "EUR",
        }
        resp = requests.get("https://api.goclimateneutral.org/v1/flight_footprint", auth=requests.auth.HTTPBasicAuth(API_KEY, ""), data=req)
        if resp.status_code == 200:
            cache[key] = resp.json()
    else:
        print("Cache hit \\o/ %s" % key)
    line["co2_exact"] = cache[key]["footprint"]
    print(cache[key])
    fixed.writerow(line)