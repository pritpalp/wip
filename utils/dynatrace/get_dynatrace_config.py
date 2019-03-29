import requests
import os
import json
import io

# Constants
API_STRING = "?Api-Token="
API_VERSION = "/api/config/v1"
API_KEY = os.getenv("API_KEY")
DYNATRACE_URL = os.getenv("DYNATRACE_URL")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")
PATH = os.getenv("DYNATRACE_CONF_PATH")

def write_file(filename, contents):
  # create a file if we need one and write the contents to it
  f = io.open(PATH+filename, "w+", encoding="utf-8")
  json_contents = json.loads(contents)
  f.write((json.dumps(json_contents, sort_keys=True, indent=2, separators=(',', ': ')).decode('utf-8')))
  f.close


def do_request(action):
  # send a request to the server and return the response
  return requests.get(action)


def config_to_get(url_part, get_what, params="NONE", multipart="FALSE"):
  # construct the url, send the request to the server, and write out the response to file
  if params is "NONE":
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_STRING+API_KEY
  else:
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_STRING+API_KEY+params
  filename = get_what + ".json"
  server_response = do_request(action)
  print action + "\n"
  print server_response.content.decode('utf-8')
  write_file(filename, server_response.content.decode('utf-8'))
  if multipart is "TRUE":
    json_repsonse = json.loads(server_response.content.decode('utf-8'))
    json_root_element = "values"
    # hack for dashboards json, has a dashboards 'object' rather than 'values'
    if "dashboards" in url_part:
      json_root_element = "dashboards"
    for ids in json_repsonse[json_root_element]:
      # should I put the id into the filename instead of name...
      new_url_part = url_part + "/" + ids['id']
      new_get_what = (get_what + "__" + ids['name']).replace(" ", "_")
      # hack for dashboards json, name can be the same for multiple users/owners
      if "dashboards" in url_part:
        new_get_what = (get_what + "__" + ids['name'] + "___" + ids['owner']).replace(" ", "_")
      config_to_get(new_url_part, new_get_what)


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
config_to_get("/dashboards", "dashboards", "NONE", "TRUE")
