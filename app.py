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
    print(dialog_intent)
    print(dialog_request)
    if dialog_intent == 'events.search':
        pass
    params = parse_params(dialog_intent, dialog_request)
    if params:
        search_query = dialog_request['queryResult']['parameters'][params[0]]
    else: search_query = "marathon"

    #Lots of processing
    answer = Answer.Answer()
    cards = []
    items = []
    suggestions = []
    api_responses = eventfinda_api.query_ef_api(search_query)
    #answer.add_followupEventInput("eventsearch-followup",[])
    if api_responses:
        answer.add_google_payload()
        answer.test_list()
        #test answer
        #----------------------------------------------------------------------------------#
        # handbreak = 0
        # for event in api_responses:
        #     name = event['name']
        #     description = event['description']
        #     image_url = event['images']['images'][0]['transforms']['transforms'][3]['url']
        #     button = [{"text": "button text","postback": "http://assistant.google.com/"}]
        #     card = answer.create_card(title=name,card_text=description,image_url=image_url)
        #     item = answer.create_item(name,description,image_url)
        #     suggestion = name
        #     #print(card)
        #     if handbreak < 3:
        #         answer.add_fulfillmentMessage(card)
        #         answer.add_payload(suggestion,item)
        #         handbreak = handbreak + 1
        # ----------------------------------------------------------------------------------#
        #answer.reply.pop('fulfillmentText')

    #print(answer.reply)
    if dialog_intent == "events.search - custom":
        answer = Answer.Answer()
        answer.add_google_payload()
        answer.test_basicCard()
        return Response(json.dumps(answer.reply), status=200, content_type="application/json")
    else:
        return Response(json.dumps(answer.reply), status=200, content_type="application/json")


