'''
sample code from https://www.eventfinda.sg/api/v2/overview#python

https://www.eventfinda.sg/api/v2/events

'''

# import json, urllib2, base64
import base64
import json
import random
from urllib.request import urlopen, Request

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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


def searchEventsByFreeText(queryText, simpleResponse):
    url = f"http://api.eventfinda.sg/v2/events.json?q=({queryText})&rows=5"  # ok

    data = call_api(url)

    fulfillmentMessages = []
    suggestions = []
    items = []
    image = ''
    item = ''

    fulfillmentMessages_dict = {}

    if data['@attributes']["count"] != 0:
        for event in data["events"]:
            card_button = [{"text": "More Details", "postback": 'check ' + event["name"]}]
            for image in event['images'].get('images'):
                for transform in image['transforms'].get('transforms'):
                    if transform['transformation_id'] == 8:
                        image = {"url": f"https:{transform['url']}",
                                 "accessibilityText": event["name"]
                                 }
            card = {
                "title": event["name"],
                "subtitle": event["location"]["name"] + " " + event["datetime_summary"],
                "image": image,
                "buttons": card_button
            }

            item = build_item(event["name"], event, image)

            fulfillmentMessages_dict = {"card": card}
            # fulfillmentMessages_dict = {"card": item}
            suggestions.append({"title": event["name"][:23] + '..' if len(event['name']) > 23 else event['name']})
            fulfillmentMessages.append(fulfillmentMessages_dict)
            items.append(item)

        # hack carouselSelect items 2 to 10 bug.
        if len(items) == 1:
            items.append(build_item(event["name"] + ' - 1', event, image))

        result = {
            "fulfillmentMessages": fulfillmentMessages,
            "payload": {
                "google": {
                    "expectUserResponse": "true",
                    "isSsml": "false",
                    "noInputPrompts": [],
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": simpleResponse
                                }
                            }
                        ],
                        "suggestions": suggestions
                    },
                    "systemIntent": {
                        "intent": "actions.intent.OPTION",
                        "data": {
                            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                            "carouselSelect": {
                                "items": items
                            }
                        }
                    }
                }
            }
        }

    else:
        result = {"fulfillmentText": fallback_resp[random.randrange(0, 2, 1)]}
    print("\nfulfillmentMessages:\n")
    print(result)

    # return 'We have following events: \r\n' + result + '. Which event you want to check more details?'
    return result, data


def build_item(event_name, event, image):
    item = {
        "optionInfo": {
            "key": event_name,
            "synonyms": [
                event_name
            ]
        },
        "description": event["location"]["name"] + " " + event["datetime_summary"],
        "image": image,
        "title": event_name
    }
    return item


def recommends(filename, searchQuery):
    querysDF = pd.read_csv(filename)
    # print('Raw Data: ', querysDF, '\n')

    # loading queryText dataType historical data.
    querysDF = querysDF[querysDF['dataType'] == 'queryText']
    querysDF['rawContent'] = querysDF['rawContent'].str.lower()
    # print('filtered result: ', querysDF[querysDF['dataType'] == 'queryText'], '\n')
    all_queries = querysDF.groupby('session_id')['rawContent'].apply(lambda s: "%s" % ','.join(s))
    # print("Past Queries, ", session_queries.values, '\n')

    # build tfidf recommendation sparse matrix.
    tfidf = TfidfVectorizer()
    queries_tfidf = tfidf.fit_transform(all_queries.values)

    # search by similarity. second best. Best match maybe in same history and results in empty recommendation.
    vals = cosine_similarity(tfidf.transform([searchQuery.lower()]), queries_tfidf).argsort()[0][::-1]
    possible_recommendations_set = ''

    # loop until no empty set from set.difference()
    for i in vals:
        matchedString = all_queries.values[i]
        print('searched', searchQuery, ' result: ', matchedString)

        # excluded search keywords.
        possible_recommendations_set = set(matchedString.split(',')).difference(set(searchQuery.split(',')))
        if len(possible_recommendations_set) > 0:
            break

    # print('possible recommendations: ', possible_recommendations_set)
    recommendations = list(possible_recommendations_set)
    # print(recommendations)

    # returns 1 recommendations randomly.
    result = random.choice(recommendations)
    return result
