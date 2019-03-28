import requests
import os

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
  response = requests.get(action)
  server_response = ""
  if response.status_code == 200:
    server_response = response.content.decode('utf-8')
  return server_response


def config_to_get(url_part, get_what, params="NONE"):
  # construct the url, send the request to the server, and write out the response to file
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

# Anomaly Detection - Services
config_to_get("/anomalyDetection/services", "services_anomaly_detection")

# Anomaly Detection - Metric events
# **** Need to expand this out and get the individual entities ****
config_to_get("/anomalyDetection/metricEvents", "metric_anomaly_detection", "&includeEntityFilterMetricEvents=true")

# Application detection configuration
# **** Need to expand this out and get the individual entities ****
config_to_get("/applicationDetectionRules", "app_detection_config")

# Automatically applied tags
# **** Need to expand this out and get the individual entities ****
config_to_get("/autoTags", "auto_tags")

# Dashboards
# **** Need to expand this out and get the individual entities ****
config_to_get("/dashboards", "dashboards")

# Maintenance windows
# **** Need to expand this out and get the individual entities ****
config_to_get("/maintenanceWindows", "maintenance")

# Management zones
# **** Need to expand this out and get the individual entities ****
config_to_get("/managementZones", "management_zones")
