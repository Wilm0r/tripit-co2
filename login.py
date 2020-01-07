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

import sys

import tripit

def main(argv):
    api_url = "https://api.tripit.com"
    consumer_key = "a5c76f91ba397d94a3129a2b86889e11ba998259"
    consumer_secret = "18e27c9af57f274c30347b1740194f06b6442d6b"

    oauth_credential = tripit.OAuthConsumerCredential(oauth_consumer_key=consumer_key, oauth_consumer_secret=consumer_secret)
    t = tripit.TripIt(oauth_credential, api_url = api_url)
    pokke = t.get_request_token()
    print pokke
    print "https://www.tripit.com/oauth/authorize?oauth_token=%(oauth_token)s&oauth_callback=https://www.bitlbee.org/main.php/oauth2.html" % pokke

    raw_input("Open that in your browser and hit enter when it's done. (Ignore the bitlbee.org page it forwards you to.)")
    
    oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret, pokke["oauth_token"], pokke["oauth_token_secret"])
    t = tripit.TripIt(oauth_credential, api_url = api_url)
    takke = t.get_access_token()
    
    print(" ".join([api_url, consumer_key, consumer_secret, "%(oauth_token)s %(oauth_token_secret)s" % takke]))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
