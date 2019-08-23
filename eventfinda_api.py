import requests
import json
from requests.auth import HTTPBasicAuth

import config as cfg

USERNAME = cfg.Config.EF_API_USERNAME
PASSWORD = cfg.Config.EF_API_PASSWORD
URL = cfg.Config.EF_GEN_URL

def parse_response(data):
    try:
        json_data = json.loads(data)
        #What data do we need ?
        events = json_data['events']
        return events
    except json.JSONDecodeError:
        #change to logger
        print("Data mismatch!")

def query_ef_api(query):
    request_url = URL%(query)
    print(request_url)
    response = requests.get(request_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.ok:
        return parse_response(response.content)