import requests
import os
import json

# Constants
API_TOKEN = "?Api-Token="
API_VERSION = "/api/config/v1"
API_KEY = os.getenv("API_KEY")
DYNATRACE_URL = os.getenv("DYNATRACE_URL")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")
PATH = os.getenv("DYNATRACE_CONF_PATH")

def write_file(filename, contents):
  # create a file if we need one and write the contents to it
  f = open(PATH+filename, "w+")
  f.write(contents)
  f.close


def do_request(action):
  # send a request to the server and return the response
  return requests.get(action)


def config_to_get(url_part, get_what, params="NONE", multipart="FALSE"):
  # construct the url, send the request to the server, and write out the response to file
  if params is "NONE":
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_TOKEN+API_KEY
  else:
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_TOKEN+API_KEY+params
  filename = get_what + ".json"
  original_get_what = get_what
  get_what = do_request(action)
  write_file(filename, get_what.content.decode('utf-8'))
  print action + "\n"
  if multipart is "TRUE":
    json_repsonse = json.loads(get_what.content.decode('utf-8'))
    for ids in json_repsonse["values"]:
      # should I put the id into the filename instead of name...
      config_to_get(url_part + "/" + ids['id'], (original_get_what + "__" + ids['name']).replace(" ", "_"))


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

# Anomaly Detection - Services
config_to_get("/anomalyDetection/services", "services_anomaly_detection")

# Anomaly Detection - Metric events
config_to_get("/anomalyDetection/metricEvents", "metric_anomaly_detection", "&includeEntityFilterMetricEvents=true", "TRUE")

# Application detection configuration
config_to_get("/applicationDetectionRules", "app_detection_config", "NONE", "TRUE")

# Automatically applied tags
config_to_get("/autoTags", "auto_tags", "NONE", "TRUE")

# Maintenance windows
config_to_get("/maintenanceWindows", "maintenance", "NONE", "TRUE")

# Management zones
config_to_get("/managementZones", "management_zones", "NONE", "TRUE")

# Dashboards
# **** Need to fix this as the json comes back as "dashboards" rather than "values" ****
#config_to_get("/dashboards", "dashboards", "NONE", "TRUE")
