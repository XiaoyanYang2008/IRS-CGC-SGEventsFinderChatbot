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

fallback_resp = ["Sorry. I do not understand. Can you please rephrase?",
                 "I did not get your response. Can you please try again?", "I missed what you said. What was that?"]
resp_prefix = ["Here is an event for you.\n", "You might be interested in this event.\n",
               "Here is an event you might be interested in.\n"]


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


def searchEventsByFreeText(queryText):
    url = f"http://api.eventfinda.sg/v2/events.json?q=({queryText})&rows=5"  # ok

    data = call_api(url)

    fulfillmentMessages = []
    image = ''

    if data['@attributes']["count"] != 0:
        for event in data["events"]:
            card_button = [{"text": "More Details...", "postback": event["url"]}]
            for image in event['images'].get('images'):
                for transform in image['transforms'].get('transforms'):
                    if transform['transformation_id'] == 8:
                        image = {"url": f"https:{transform['url']}"}
            card = {
                "title": event["name"],
                "subtitle": event["location"]["name"] + " " + event["datetime_summary"],
                "image": image,
                "buttons": card_button
            }
            fulfillmentMessages_dict = {"card": card}
            fulfillmentMessages.append(fulfillmentMessages_dict)

        result = {"fulfillmentMessages": fulfillmentMessages}

    else:
        result = {"fulfillmentText": fallback_resp[random.randrange(0, 2, 1)]}

    print(result)

    # return 'We have following events: \r\n' + result + '. Which event you want to check more details?'
    return result
