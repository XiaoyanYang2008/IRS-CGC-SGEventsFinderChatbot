from flask import Flask, Response, request

from eventfindaClient import *
from util import *

app = Flask(__name__)

coin_dct = construct_coin_dct()


def getPriceIntentHandler(coinname):
    coinname = "".join(coinname.split())
    price = getprice(coinname, coin_dct)
    return f"The price of {coinname} is {price}"


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
        resp_text = searchEventsByFreeText(queryText)
    else:
        resp_text = "Unable to find a matching intent. Try again."

    resp = {
        "fulfillmentText": resp_text
    }

    return Response(json.dumps(resp), status=200, content_type="application/json")


app.run(host='0.0.0.0', port=5001, debug=True)
