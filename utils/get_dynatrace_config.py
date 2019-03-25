#!/bin/python
import requests
import json

API_TOKEN = "?Api-Token="
API_KEY = ""
DYNATRACE_URL = ""
API_VERSION = "/api/config/v1"
ENVIRONMENT_ID = ""

def do_request(action):
  req_url = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+action+API_TOKEN+API_KEY
  response = requests.get(req_url)
  server_response = ""
  if response.status_code == 200:
    server_response = json.loads(response.content.decode('utf-8'))
  print req_url, "\n"
  print server_response, "\n\n"
  return server_response

# Web application config
# we only have one application, so can just grab the default config
action = "/applications/web/default"
web_app_config = do_request(action)

# Anomoly Detection - Applications
action = "/anomalyDetection/applications"
app_anomoly_detection = do_request(action)
