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

    params = parse_params(dialog_intent, dialog_request)
    if params:
        search_query = dialog_request['queryResult']['parameters'][params[0]]
    else: search_query = "marathon"

    #Lots of processing
    if dialog_intent == 'events.search':
        answer = Answer.Answer()
        api_responses = eventfinda_api.query_ef_api(search_query)
        #answer.add_followupEventInput("eventsearch-followup",[])
        if api_responses:
            answer.add_google_payload()
            answer.add_richResponse()
            answer.add_richResponseItem(answer.create_simpleResponse("Here are your results"))
            answer.add_systemIntent()
            items = []
            handbreak = 5
            for event in api_responses:
                name = event['name']
                description = event['description']
                image_url = event['images']['images'][0]['transforms']['transforms'][3]['url']

                if handbreak > 0:
                    items.append(answer.create_listItems(name,name,description,answer.create_richImage(image_url,name)))
                    handbreak = handbreak - 1
            answer.add_listSelect("Query Results",items)
        print(answer.reply)
        return Response(json.dumps(answer.reply), status=200, content_type="application/json")

    if dialog_intent == "events.search - custom":
        answer = Answer.Answer()
        answer.add_google_payload()
        answer.add_richResponse()
        answer.add_richResponseItem(answer.create_simpleResponse("Okay..."))
        basicCard = answer.create_basicCard("Hello","Hello World!","Ipsum lorme bleh  Okay one two three \\ four five six seven.",answer.create_richImage("//cdn.eventfinda.sg/uploads/events/transformed/42063-19086-27.jpg","image"),answer.create_basicCardButton("Click Me","https://google.com"))
        answer.add_richResponseItem(basicCard)
        #answer.add_systemIntent()
        return Response(json.dumps(answer.reply), status=200, content_type="application/json")
    # else:
    #     return Response(json.dumps(answer.reply), status=200, content_type="application/json")


