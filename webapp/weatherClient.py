from flask import Flask, request, Response
import json
import requests

app = Flask(__name__)
APIKEY = "8a81d247d650cb16469c4ba3ceb7d265"


def getjson(url):
    resp = requests.get(url)
    return resp.json()


def getWeatherInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
    print(data)
    return data


def getWeatherText(req):
    location = req["queryResult"]["parameters"]["location"]
    wind = req["queryResult"]["parameters"]["wind"]
    temperature = req["queryResult"]["parameters"]["temperature"]
    weather = req["queryResult"]["parameters"]["weather"]

    if wind != '' or temperature != '' or weather != '':
        return getWeatherIntentHandler(location)
    else:
        return "Sorry, i didn't get your question!"


def getWeatherIntentHandler(location):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    if "street-address" in location and location["street-address"] != '':
        area = location["street-address"]
    elif "city" in location and location["city"] != '':
        area = location["city"]
    elif "country" in location and location["country"] != '':
        area = location["country"]
    else:
        area = "Singapore"

    data = getWeatherInfo(area)
    weather = data["weather"][0]["description"]
    if data["main"]["temp"] != '':
        temp = round((data["main"]["temp"] - 272.15), 1)
        weather = weather + ", Temperature: " + str(temp) + "°C"
    if data["wind"]["speed"] != '':
        wind = checkWindScale(data["wind"]["speed"])
        weather = weather + ", Wind: " + wind
    return f"Currently, the weather in {area} is {weather}"


# check wind scale
def checkWindScale(speed):
    if speed < 1:
        wind = "Calm"
    elif speed < 6:
        wind = "Light air"
    elif speed < 12:
        wind = "Light"
    elif speed < 20:
        wind = "Gentle"
    elif speed < 29:
        wind = "Moderate"
    elif speed < 38:
        wind = "Fresh"
    elif speed < 50:
        wind = "Near gale"
    elif speed < 75:
        wind = "Gale"
    elif speed < 89:
        wind = "Strong"
    elif speed < 103:
        wind = "Storm"
    elif speed < 118:
        wind = "Violent"
    else:
        wind = "Hurricane force"

    return wind + " with speed " + str(speed) + "km/h"
