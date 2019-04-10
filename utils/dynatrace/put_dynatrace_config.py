import requests
import os
import json
import io
import yaml

# Constants
API_STRING = "?Api-Token="
API_VERSION = "/api/config/v1"

# Pulled from environement variables
CONFIG_FILE = os.getenv("DYNATRACE_CONFIG_FILE")
API_KEY = os.getenv("API_KEY")
DYNATRACE_URL = os.getenv("DYNATRACE_URL")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")
PATH = os.getenv("DYNATRACE_CONF_PATH")

# so we should be able to use requests to post back to the server with the json as a payload
# task one...read the json and grab the id from it
filename = "maintenance__Weekly_release.json"
f = io.open(PATH+filename, "r", encoding="utf-8")
test = f.read()
# put it into a json object
content = json.loads(test)
f.close()
# print the file we load
print test
# print out a nice looking file
print json.dumps(content, sort_keys=True, indent=2, separators=(',', ': ')).decode('utf-8')
# find the id...
id = ""
for (k, v) in content.items():
  if "id" in k:
    id = str(v)
    break
print "id:", id
