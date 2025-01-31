#!/usr/bin/python3

import json
from pprint import pprint
from lib import http

#r = http.post('https://httpbun.com/post', '{"moo": 1}', headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
#pprint(json.loads(r))

#pprint(http.post_json('https://httpbun.com/post', {"moo": 1}))
#pprint(http.get_json('https://httpbun.com/get?moo=1'))
#print(http.get('https://httpbun.com/get?moo=1'))

pprint(http.delete('https://httpbun.com/delete', data='{"moo": 1}', retries=0, retry_delay=1))
