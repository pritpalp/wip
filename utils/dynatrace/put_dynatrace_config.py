import requests
import os
import json
import io
import yaml

# Constants
API_STRING = "?Api-Token="
API_VERSION = "/api/v1"  # for hosted "/api/config/v1"

# Pulled from environement variables
CONFIG_FILE = os.getenv("DYNATRACE_CONFIG_FILE")
API_KEY = os.getenv("API_KEY")
DYNATRACE_URL = os.getenv("DYNATRACE_URL")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")
PATH = os.getenv("DYNATRACE_CONF_PATH")

# We can do...
# 1. Post/Put all config that we find
# 2. Post/Put config based on the configuration file

# so we should be able to use requests to post back to the server with the json as a payload
# task one...read the json and grab the id from it
filename = "maintenance__Weekly_release.json"

def read_file(filename):
  f = io.open(PATH+filename, "r", encoding="utf-8")
  test = f.read()
  content = json.loads(test)
  f.close()
  return content


# do we need this function?
def get_id(content):
  # find the id...
  id = ""
  for (k, v) in content.items():
    if "id" in k:
      id = str(v)
      break
  print "id:", id
  return id


def put_request(action, content):
  # task two, send a post and check the response
  # construct the url
  #url = "https://qas17954.sprint.dynatracelabs.com/api/v1/maintenance?Api-Token=O5sKgj9_Rs2kKc_1KTyKK"
  action = DYNATRACE_URL+API_VERSION+"/maintenance"+API_STRING+API_KEY
  # we get a ssl error to do with the self signed cert on the test env, so have to set verify=False
  headers = {'content-type' : 'application/json'}
  # we should be able to just set json=content or something and not worry about setting headers,
  # but the api is different in my test env
  r = requests.put(action, data=json.dumps(content), verify=False, headers=headers)
  print r.status_code
  print r.content
