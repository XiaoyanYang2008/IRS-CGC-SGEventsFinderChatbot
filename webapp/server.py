import csv
import os

from flask import Flask, Response, request

import weatherClient
from eventfindaClient import *

DATATYPE_EVENTS_BY_FREE_TEXT_DATA = 'searchEventsByFreeTextData'

DATATYPE_QUERY_TEXT = 'queryText'

FILE_SESSION_DATA_CSV = os.path.join('db', 'session-data.csv')

app = Flask(__name__)

'''
recommendation:
build queries into csv for a given sessionid
td-idf  and cons-similarity
search, unseperate, remove similar keys,

'''


def parseSessionID(session_id_str):
    if session_id_str is None or session_id_str == '':
        return ''

    chunks = session_id_str.split('/')
    session_id = chunks[len(chunks) - 1]
    return session_id


def insertData(filename, session_id, dataType, rawContent):
    # Insert data into csv file
    try:
        header = ['session_id', 'dataType', 'rawContent']
        data = [session_id, dataType, rawContent]

        if not os.path.exists(filename):
            with open(filename, "w") as tmp:
                wh = csv.writer(tmp, quoting=csv.QUOTE_NONE)
                wh.writerow(header)
                tmp.close()

        with open(filename, "a+") as fp:
            wr = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(data)
            fp.close()

        return "Data of " + session_id + " created successfully"

    except Exception as e:
        errmsg = "Error encountered: " + str(e)
        return errmsg


@app.route("/", methods=["POST"])
def main():
    req = request.get_json(silent=True, force=True)
    print(req)

    session_id = parseSessionID(req['session'])  # use this as key to accumulate baskets of search key words

    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "SearchEvent":
        queryText = req["queryResult"]["parameters"]["queryText"]

        queryText = (("+".join(queryText)).replace(" ", "-")).lower()

        insertData(FILE_SESSION_DATA_CSV, session_id, DATATYPE_QUERY_TEXT, queryText)
        resp, data = searchEventsByFreeText(queryText, "Here are the results: ")
        # insertData(FILE_SESSION_DATA_CSV, session_id, DATATYPE_EVENTS_BY_FREE_TEXT_DATA, data)

    elif intent_name == "Recommendation":

        df = pd.read_csv(FILE_SESSION_DATA_CSV)

        df_session = df[df['session_id'] == session_id]

        queryText = ''

        if not df_session.empty:
            searchQuery = df_session.groupby('session_id')['rawContent'].apply(lambda s: "%s" % ','.join(s)).values[
                0].lower()

            queryText = recommends(FILE_SESSION_DATA_CSV, searchQuery)

            resp, data = searchEventsByFreeText(queryText,
                                                "We recommends " + queryText + ". And here are the results: ")
            # insertData(FILE_SESSION_DATA_CSV, session_id, DATATYPE_EVENTS_BY_FREE_TEXT_DATA, data)
        else:
            resp = {
                "fulfillmentText": "Please search some events first before recommendations."
            }
        # queryText = req["queryResult"]["parameters"]["queryText"]
        # insertData(FILE_SESSION_DATA_CSV, session_id, DATATYPE_QUERY_TEXT, queryText)
        #
        # queryText = (("+".join(queryText)).replace(" ", "-")).lower()

    elif intent_name == "SearchEvent - viewdetails":
        print("SearchEvent - View Details")
        if req["queryResult"]["queryText"] == "actions_intent_OPTION":
            outputContext = req["originalDetectIntentRequest"]["payload"]["inputs"][0]["arguments"][0]["textValue"]
            outputContext = outputContext.replace("view detail of ", "")
        outputContext = (outputContext.replace(" - ", "-")).lower()
        outputContext = outputContext.replace(" ", "-")
        #outputContext = outputContext.encode("utf-8")
        resp, data = viewEventDetail(outputContext)

    elif intent_name == "GetWeather":
        resp = weatherClient.getWeatherText(req)

    else:
        resp = {
            "fulfillmentText": "Unable to find a matching intent. Try again."
        }

    return Response(json.dumps(resp), status=200, content_type="application/json")


app.run(host='0.0.0.0', port=5001, debug=True)
