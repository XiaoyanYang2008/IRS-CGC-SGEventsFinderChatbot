# @author: Tarun Rajkumar

class Answer:
    def __init__(self):
        self.reply = {"fulfillmentText": "This is a text response",
                      "fulfillmentMessages":[],
                      "outputContexts":[]}

    def add_fulfillmentText(self,respone_text):
        self.reply['fulfillmentText']=respone_text

    def add_fulfillmentMessage(self,card):
        self.reply['fulfillmentMessages'].append(card)

    def create_card(self,title,card_text,image_url,button=None):
        if button:
            return {"card": {
                "title": title,
                "subtitle": card_text,
                "imageUri": image_url,
                "buttons": button
            }}
        return {"card":{
            "title":title,
            "subtitle":card_text,
            "imageUri":image_url
        }}

    def add_outputContexts(self,name,lifespanCount,parameters):
        self.reply['outputContexts'].append({
            "name":name,
            "lifespanCount":lifespanCount,
            "parameters":parameters
        })

    def add_followupEventInput(self,name,parameters,languageCode="en-US"):
        self.reply["followupEventInput"] = dict(name=name, languageCode=languageCode, parameters=parameters)
