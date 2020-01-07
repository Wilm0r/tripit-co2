#!/usr/bin/env python2
#
# Copyright 2008-2012 Concur Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import print_function   # wtf python2?

import csv
import sys
from xml.etree import cElementTree as etr
import re

import tripit

def main(argv):
    if len(argv) < 5:
        print("Usage: co2.py api_url consumer_key consumer_secret authorized_token authorized_token_secret")
        return 1

    # Dump xml data in an intermediate file, so if you want to make any
    # changes to the code below, you can test without triggering new API
    # calls on every run. (Just set this if to False.)
    if True:
        api_url = argv[0]
        consumer_key = argv[1]
        consumer_secret = argv[2]
        authorized_token = argv[3]
        authorized_token_secret = argv[4]

        oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret, authorized_token, authorized_token_secret)
        t = tripit.TripIt(oauth_credential, api_url = api_url)

        t.list_object({"include_objects": "true", "past": "true", "type": "air"})
        open("flights.xml", "w").write(t.response)

    # Can't believe I still have to deal with decrepit Python2 without
    # ordered dicts!
    columns = [('who',
                ['../Traveler/first_name',
                 '../Traveler/middle_name',
                 '../Traveler/last_name']),
               ('date', 'StartDateTime/date'),
               ('src', 'start_airport_code'),
               ('dst', 'end_airport_code'),
               ('flight', ['marketing_airline_code',
                           'marketing_flight_number']),
               ('aircraft', 'aircraft'),
               ('aircraft_desc', 'aircraft_display_name'),
               ('distance', 'distance'),
               ('class', 'service_class'),
               ('co2', 'Emissions/co2'),
               ('class_exact', ''),
               ('co2_exact', '')]

    parsed = etr.fromstring(open("flights.xml", "r").read())
    out = csv.writer(open("co2.csv", "w"))
    out.writerow([k for k, v in columns])
    for trip in parsed:
        for seg in trip.findall("Segment"):
            ret = {}
            for k, v in columns:
                val = ""
                if not isinstance(v, list):
                    v = [v]
                for path in v:
                    if path.startswith("../"):
                        el = trip.find(path[3:])
                    else:
                        el = seg.find(path)
                    if el is not None:
                        val += el.text
                ret[k] = val
            who = ret["who"]
            # Modify this if your results contain trips of TripIt
            # contacts of yours.
            #if who and not ("wilmer" in who.lower()):
            #    continue
            if ret["distance"].endswith("km"):
                ret["distance"] = re.sub(r"[^0-9]", "", ret["distance"])
            rc = ret["class"].lower()
            if not ret["distance"]:
                # Skip corrupt entries. (Had some from Jeju Air)
                continue
            # Vague attempt at converting at least BA terminology.
            if "club" in rc:
                ret["class_exact"] = "business"
            elif "first" in rc:
                ret["class_exact"] = "first"
            elif "plus" in rc:
                ret["class_exact"] = "premium_economy"
            elif "premium" in rc:
                ret["class_exact"] = "premium_economy"
            elif int(ret["distance"]) > 4000:
                # And then resort to my own rule of never flying economy
                # unless it's short-haul.
                ret["class_exact"] = "premium_economy"
            else:
                ret["class_exact"] = "economy"
            print(ret)
            out.writerow([ret[k] for k, v in columns])   # Yeah seriously man, fucking Python2..

        
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
