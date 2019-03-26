#!/bin/python
import requests

# Constants
API_TOKEN = "?Api-Token="
API_KEY = ""
DYNATRACE_URL = ""
API_VERSION = "/api/config/v1"
ENVIRONMENT_ID = ""

def write_file(filename, contents):
  # create a file if we need one
  f = open(filename, "w+")
  f.write(contents)
  f.close


def do_request(action):
  req_url = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+action+API_TOKEN+API_KEY
  response = requests.get(req_url)
  server_response = ""
  if response.status_code == 200:
    server_response = response.content.decode('utf-8')
  # print out to screen...
  print req_url, "\n"
  return server_response


# Web application config
# we only have one application, so can just grab the default config
action = "/applications/web/default"
web_app_config = do_request(action)
write_file("web_app_config.json", web_app_config)

# Anomaly Detection - Applications
action = "/anomalyDetection/applications"
app_anomaly_detection = do_request(action)
write_file("app_anomaly_detection.json", app_anomaly_detection)

# Anomaly Detection - AWS
action = "/anomalyDetection/aws"
aws_anomaly_detection = do_request(action)
write_file("aws_anomaly_detection.json", aws_anomaly_detection)

# Anomaly Detection - DB services
action = "/anomalyDetection/databaseServices"
db_anomaly_detection = do_request(action)
write_file("db_anomaly_detection.json", db_anomaly_detection)
