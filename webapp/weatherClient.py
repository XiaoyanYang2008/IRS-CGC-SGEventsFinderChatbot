from flask import Flask
import datetime
import requests

app = Flask(__name__)

def getWeatherText(req):
    weatherurl = "https://www.nea.gov.sg/weather"
    weatherText = req["queryResult"]["parameters"]["weather"]
    weatherdate = req["queryResult"]["parameters"]["date"].split('T')[0]
    weatherdate = datetime.date(*(int(s) for s in weatherdate.split('-')))

    if weatherText != '':
        fulfillmentMessages, weatherText = getWeatherMessage(weatherdate)
        card = setCard(weatherText)
        fulfillmentMessages_dict = {"card": card}
        fulfillmentMessages.append(fulfillmentMessages_dict)

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
                                    "textToSpeech": f"{weatherText}"
                                }
                            }
                        ]

                    }
                }
            }
        }
        return result
    else:
        return {"fulfillmentText": "Sorry, i didn't get your question!"}


def getWeatherMessage(weatherdate):
    today = datetime.datetime.today().date()
    deltaDate = weatherdate - today
    if deltaDate.days == 0:
        API_ENDPOINT = f"https://api.data.gov.sg/v1/environment/24-hour-weather-forecast?date={today}"
    else:
        API_ENDPOINT = f"https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date={today}"
    resp = requests.get(API_ENDPOINT)
    fulfillmentMessages = []
    weatherJson = resp.json()
    if deltaDate.days == 0:
        deltadays = deltaDate.days
        forecast = weatherJson["items"][deltadays]["general"]
    else:
        deltadays = deltaDate.days - 1
        forecast = weatherJson["items"][0]["forecasts"][deltadays]
    temperature = str(forecast["temperature"]["low"]) + "°C~" + str(forecast["temperature"]["high"]) + "°C"
    wind_speed = str(forecast["wind"]["speed"]["low"]) + "km/h~" + str(forecast["wind"]["speed"]["high"]) + "km/h"
    message = f"The weather on {weatherdate} is: "
    weatherText = message + forecast["forecast"] + "\n Temperature: " + temperature + ", Wind speed: " + wind_speed
    return fulfillmentMessages, weatherText


def setCard(weatherText):
    card_button = [{"text": "More Details", "postback": 'check ' + weatherText}]
    card = {
        "title": "Weather forecast",
        "subtitle": weatherText,
        "buttons": card_button
    }
    return card


def setItem(weatherText):
    item = {
        "optionInfo": {
            "key": "Weather forecast",
            "synonyms": [
                "Weather forecast"
            ]
        },
        "description": weatherText,
        "title": "Weather forecast"
    }
    return item
