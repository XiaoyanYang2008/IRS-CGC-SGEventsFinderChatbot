from flask import Flask, Request, Response, request
import json
import config
import Answer
import eventfinda_api

app = Flask(__name__)
app.config.from_object('config')

def parse_params(intent, data):

    dialog_intent  = intent
    dialog_parameters = data['queryResult']['parameters']
    valid_params = [params for params in dialog_parameters if dialog_parameters[params]]
    return valid_params

@app.route('/', methods=['POST'])
def main():
    dialog_request = request.get_json(silent=True,force=True)
    dialog_intent = dialog_request["queryResult"]["intent"]["displayName"]
    dialog_session = dialog_request['session']
    params = parse_params(dialog_intent, dialog_request)


    #Lots of processing
    answer = Answer.Answer()
    cards = []
    api_responses = eventfinda_api.query_ef_api("Cycling")

    if api_responses:

        handbreak = 0
        for event in api_responses:
            name = event['name']
            description = event['description']
            image_url = event['images']['images'][0]['transforms']['transforms'][2]['url']
            button = [{"text": "button text","postback": "http://assistant.google.com/"}]
            card = answer.create_card(title=name,card_text=description,image_url=image_url)
            #print(card)
            if handbreak < 2:
                answer.add_fulfillmentMessage(card)
                handbreak = handbreak + 1

    return Response(json.dumps(answer.reply), status=200, content_type="application/json")


