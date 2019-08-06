'''
sample code from https://www.eventfinda.sg/api/v2/overview#python
'''

# import json, urllib2, base64
import base64
import json

from urllib.request import urlopen, Request

url = 'http://api.eventfinda.sg/v2/events.json?rows=2'
username = 'schoolprojectgoogleassistantchatbotforsingaporeevents';
password = 'qbvnn9ynhbt3';
request = Request(url)
# request = url
# https://stackoverflow.com/questions/31144988/base64-encodestring-failing-in-python-3
base64string = base64.encodestring(('%s:%s' % (username, password)).encode()).decode().replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

result = urlopen(request)
# print(result)
data = json.load(result)

for event in data["events"]:
    print(event["name"])
    for img in event["images"]["images"]:
        print(img['id'])
        for imgtran in img["transforms"]["transforms"]:
            print(imgtran["url"])
