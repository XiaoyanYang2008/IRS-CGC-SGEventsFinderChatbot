# @author: Tarun Rajkumar

class Answer:
    def __init__(self):
        self.reply = {}

    def add_fulfillmentText(self, respone_text):
        if not 'fulfillmentText' in self.reply.keys():
            self.reply['fulfillmentText'] = respone_text
        else:
            self.reply['fulfillmentText'] = respone_text

    def add_fulfillmentMessage(self, card):
        if not 'fulfillmentMessages' in self.reply.keys():
            self.reply['fulfillmentMessages'] = [card]
        else:
            self.reply['fulfillmentMessages'].append(card)

    def add_google_payload(self):
        if not 'payload' in self.reply.keys():
            self.reply['payload'] = {
                'google': {
                    "expectUserResponse": "true"
                }
            }

    def add_richResponse(self):
        self.reply['payload']['google']['richResponse'] = {"items": []}

    def add_richResponseItem(self, richResponseItem):
        self.reply['payload']['google']['richResponse']['items'].append(richResponseItem)

    def create_simpleResponse(self, responseText):
        return {
            "simpleResponse": {
                "textToSpeech": responseText
            }
        }

    def create_basicCard(self, title, subtile, formattedText, image, buttons, imageDisplayOptions="CROPPED"):
        return {
            "basicCard": {
                "title": title,
                "subtitle": subtile,
                "formattedText": formattedText,
                "image": image,
                "buttons": [buttons],
                "imageDisplayOptions": imageDisplayOptions
            }
        }

    def create_basicCardButton(self, title, url):
        return {
            "title": title,
            "openUrlAction": {
                "url": url
            }
        }

    def add_systemIntent(self):
        self.reply['payload']['google']['systemIntent'] = {
            "intent": "actions.intent.OPTION",
            "data": {
                "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec"
            }
        }

    def add_listSelect(self, title, items):
        self.reply['payload']['google']['systemIntent']['data']['listSelect'] = {
            "title": title,
            "items": items
        }

    def create_listItems(self, op_key, title, description, image, op_synonyms=[]):
        # Perhaps directly add items ? v2 maybe
        return {
            "optionInfo": {
                "key": op_key,
                "synonyms": op_synonyms
            },
            "description": description,
            "image": image,
            "title": title
        }

    def create_richImage(self, url, hoverText):
        return {
            "url": "https:" + url,
            "accessibilityText": hoverText
        }

    def add_suggestsions(self, suggestion):
        if not 'suggestions' in self.reply['payload']['google']['richResponse'].keys():
            self.reply['payload']['google']['richResponse']['suggestions'] = [suggestion]
        else:
            self.reply['payload']['google']['richResponse']['suggestions'].append(suggestion)

    #
    # def add_payload1(self, suggestion, item):
    #     if not 'payload' in self.reply.keys():
    #         self.reply["payload"] = {
    #             "google": {
    #                 "expectUserResponse": "true",
    #                 "isSsml": "false",
    #                 "noInputPrompts": [],
    #                 "richResponse": {
    #                     'items': [{
    #                         "simpleResponse": {
    #                             "textToSpeech": "Here are some results for you"
    #                         }
    #                     }],
    #                     'suggestions': []
    #                 },
    #                 "systemIntent": {
    #                     "intent": "actions.intent.OPTION",
    #                     "data": {
    #                         "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
    #                         "carouselSelect": {"items": []}
    #                     }
    #                 }
    #             }
    #         }
    #     self.reply['payload']['google']['richResponse']['suggestions'].append({"title": suggestion if len(suggestion) <
    #                                                                                                   23 else suggestion[
    #                                                                                                           :22] + ".."})
    #     self.reply['payload']['google']['systemIntent']['data']['carouselSelect']['items'].append(item)
    def add_outputContexts(self, name, lifespanCount, parameters):
        if 'outputContexts' in self.reply.keys():
            self.reply['outputContexts'].append({
                "name": name,
                "lifespanCount": lifespanCount,
                "parameters": parameters
            })
        else:
            self.reply['outputContexts'] = [{
                "name": name,
                "lifespanCount": lifespanCount,
                "parameters": parameters
            }]

    def test_list(self):
        self.reply['payload']['google'] = {
            "systemIntent": {
                "intent": "actions.intent.OPTION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                    "listSelect": {
                        "title": "we found for you...",
                        "items": [
                            {
                                "optionInfo": {
                                    "key": "SELECTION_KEY_ONE",
                                    "synonyms": [
                                        "synonym 1",
                                        "synonym 2",
                                        "synonym 3"
                                    ]
                                },
                                "description": "This is a description of a list item.",
                                "image": {
                                    "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                    "accessibilityText": "Image alternate text"
                                },
                                "title": "Title of First List Item"
                            },
                            {
                                "optionInfo": {
                                    "key": "SELECTION_KEY_GOOGLE_HOME",
                                    "synonyms": [
                                        "Google Home Assistant",
                                        "Assistant on the Google Home"
                                    ]
                                },
                                "description": "Google Home is a voice-activated speaker powered by the Google Assistant.",
                                "image": {
                                    "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                    "accessibilityText": "Google Home"
                                },
                                "title": "Google Home"
                            },
                            {
                                "optionInfo": {
                                    "key": "SELECTION_KEY_GOOGLE_PIXEL",
                                    "synonyms": [
                                        "Google Pixel XL",
                                        "Pixel",
                                        "Pixel XL"
                                    ]
                                },
                                "description": "Pixel. Phone by Google.",
                                "image": {
                                    "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                    "accessibilityText": "Google Pixel"
                                },
                                "title": "Google Pixel"
                            }
                        ]
                    }
                }
            },
            "richResponse": {
                "items": [
                    {
                        "simpleResponse": {
                            "textToSpeech": "Here Are some results for you:"
                        }
                    }
                ]
            }
        }

    def test_basicCard(self):
        self.reply['payload']['google'] = {"richResponse": {
            "items": [
                {
                    "simpleResponse": {
                        "textToSpeech": "Here's an example of a basic card."
                    }
                },
                {
                    "basicCard": {
                        "title": "Title: this is a title",
                        "subtitle": "This is a subtitle",
                        "formattedText": "This is a basic card.  Text in a basic card can include \"quotes\" and\n    most other unicode characters including emoji 📱.  Basic cards also support\n    some markdown formatting like *emphasis* or _italics_, **strong** or\n    __bold__, and ***bold itallic*** or ___strong emphasis___ as well as other\n    things like line  \nbreaks",
                        "image": {
                            "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                            "accessibilityText": "Image alternate text"
                        },
                        "buttons": [
                            {
                                "title": "This is a button",
                                "openUrlAction": {
                                    "url": "https://assistant.google.com/"
                                }
                            }
                        ],
                        "imageDisplayOptions": "CROPPED"
                    }
                },
                {
                    "simpleResponse": {
                        "textToSpeech": "Which response would you like to see next?"
                    }
                }
            ]
        }
        }

    def add_followupEventInput(self, name, parameters, languageCode="en-US"):
        self.reply["followupEventInput"] = dict(name=name, languageCode=languageCode, parameters=parameters)

    def create_card(self, title, card_text, image_url, button=None):
        if button:
            return {"card": {
                "title": title,
                "subtitle": card_text,
                "imageUri": image_url,
                "buttons": button
            }}
        return {"card": {
            "title": title,
            "subtitle": card_text,
            "imageUri": image_url
        }}

    def create_item(self, name, description, image_url):
        return {"optionInfo": {
            "key": name,
            "synonyms": [
                name
            ]
        },
            "description": description,
            "image": {"url": "https:" + image_url, 'accessibilityText': name},
            "title": name
        }

    def add_BrowseCarouselItem(self):
        # self.reply['payload']['google']['systemIntent']['data']['']
        pass

    def create_BrowseCarouselItem(self, name, url, description, image):
        pass
