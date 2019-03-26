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
  response = requests.get(action)
  server_response = ""
  if response.status_code == 200:
    server_response = response.content.decode('utf-8')
  return server_response


def config_to_get(url_part, get_what, params="NONE"):
  if params is "NONE":
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_TOKEN+API_KEY
  else:
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_TOKEN+API_KEY+params
  filename = get_what + ".json"
  get_what = do_request(action)
  write_file(filename, get_what)
  print action + "\n"


# Web application config
# we only have one application, so can just grab the default config
config_to_get("/applications/web/default", "web_app_config")

# Anomaly Detection - Applications
config_to_get("/anomalyDetection/applications", "app_anomaly_detection")

# Anomaly Detection - AWS
config_to_get("/anomalyDetection/aws", "aws_anomaly_detection")

# Anomaly Detection - DB services
config_to_get("/anomalyDetection/databaseServices", "db_anomaly_detection")

# Anomaly Detection - Hosts
config_to_get("/anomalyDetection/hosts", "host_anomaly_detection")

# Anomaly Detection - Metric events
# **** Need to expand this out and get the individual entities ****
config_to_get("/anomalyDetection/metricEvents", "metric_anomaly_detection", "&includeEntityFilterMetricEvents=true")
