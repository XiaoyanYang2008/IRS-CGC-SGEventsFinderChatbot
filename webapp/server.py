from flask import Flask, Response, request
import random

from eventfindaClient import *
from util import *

app = Flask(__name__)


@app.route("/", methods=["POST"])
def main():
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "GetPriceIntent":
        coinname = req["queryResult"]["parameters"]["coinname"]
        resp_text = getPriceIntentHandler(coinname)
    elif intent_name == "SearchEvent":
        queryText = req["queryResult"]["parameters"]["queryText"]
        queryText = (("+".join(queryText)).replace(" ", "-")).lower()
        resp = searchEventsByFreeText(queryText)
        # resp = getEventIntentHandler(req)
    else:
        resp = {
            "fulfillmentText": "Unable to find a matching intent. Try again."
        }

    return Response(json.dumps(resp), status=200, content_type="application/json")


app.run(host='0.0.0.0', port=5001, debug=True)
