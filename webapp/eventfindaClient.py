'''
sample code from https://www.eventfinda.sg/api/v2/overview#python

https://www.eventfinda.sg/api/v2/events

'''

# import json, urllib2, base64
import base64
import json

from urllib.request import urlopen, Request

# url_slugs doesn't seems to work category_slug works for

# url = 'http://api.eventfinda.sg/v2/events.json?rows=5'  # ok
# url = 'http://api.eventfinda.sg/v2/events.json?category_slug=children-kids'  #ok.
# url = 'http://api.eventfinda.sg/v2/events.json?free=1'  # ok.
# url = 'http://api.eventfinda.sg/v2/events.json?q=(children)'  # ok

username = 'schoolprojectgoogleassistantchatbotforsingaporeevents'
password = 'qbvnn9ynhbt3'


def searchEventsByFreeText(queryText):
    url = f"http://api.eventfinda.sg/v2/events.json?q=({queryText})&rows=5"  # ok

    data = call_api(url)

    result = ''

    for event in data["events"]:
        print(event["name"])
        if result == '':
            result = event["name"]
        else:
            result = result + "; " + event["name"]

        # for img in event["images"]["images"]:
        #     print(img['id'])
        #     for imgtran in img["transforms"]["transforms"]:
        #         print(imgtran["url"])

    return 'We have following events: \r\n' + result + '. Which event you want to check more details?'


def call_api(url):
    request = Request(url)
    # request = url
    # https://stackoverflow.com/questions/31144988/base64-encodestring-failing-in-python-3
    base64string = base64.encodestring(('%s:%s' % (username, password)).encode()).decode().replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urlopen(request)
    data = json.load(result)
    print("result of ", url, " : ", data)
    return data
