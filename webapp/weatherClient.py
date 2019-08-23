from flask import Flask
import datetime
import requests

app = Flask(__name__)

def getWeatherText(req):
    weatherurl = "https://www.nea.gov.sg/weather"
    weatherText = req["queryResult"]["parameters"]["weather"]
    weatherdate = req["queryResult"]["parameters"]["date"].split('T')[0]
    weatherdate = datetime.date(*(int(s) for s in weatherdate.split('-')))
    today = datetime.datetime.today().date()
    deltaDate = weatherdate - today
    if deltaDate.days == 0:
        API_ENDPOINT = f"https://api.data.gov.sg/v1/environment/24-hour-weather-forecast?date={today}"
    else:
        API_ENDPOINT = f"https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date={today}"

    if weatherText != '':
        return getWeatherIntentHandler(API_ENDPOINT, deltaDate)
    else:
        return {"fulfillmentText": "Sorry, i didn't get your question!"}


def getWeatherIntentHandler(API_ENDPOINT, deltaDate):
    resp = requests.get(API_ENDPOINT)
    fulfillmentMessages = []
    items = []
    image = ''
    weatherJson = resp.json()
    if deltaDate.days == 0:
        deltadays = deltaDate.days
        forecast = weatherJson["items"][deltadays]["general"]
    else:
        deltadays = deltaDate.days - 1
        forecast = weatherJson["items"][0]["forecasts"][deltadays]

    temperature = str(forecast["temperature"]["low"]) + "°C~" + str(forecast["temperature"]["high"]) + "°C"
    wind_speed = str(forecast["wind"]["speed"]["low"]) + "km/h~" + str(forecast["wind"]["speed"]["high"]) + "km/h"
    weatherText = forecast["forecast"] + ", temperature is: " + temperature + ", wind speed is: " + wind_speed

    card_button = [{"text": "More Details", "postback": 'check ' + weatherText}]
    image = {"url": f"https://www.nea.gov.sg/weather"}

    card = {
        "title": "Weather forecast",
        "subtitle": weatherText,
        "image": image,
        "buttons": card_button
    }

    item = {
        "optionInfo": {
            "key": "Weather forecast",
            "synonyms": [
                "Weather forecast"
            ]
        },
        "description": weatherText,
        "image": image,
        "title": "Weather forecast"
    }
    fulfillmentMessages_dict = {"card": card}
    fulfillmentMessages.append(fulfillmentMessages_dict)

    items.append(item)
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
                                "textToSpeech": "The weather is: "
                            }
                        }
                    ],
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
    return result
