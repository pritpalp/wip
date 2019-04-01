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

def write_file(filename, contents):
  # create a file if we need one and write the contents to it
  f = io.open(PATH+filename, "w+", encoding="utf-8")
  json_contents = json.loads(contents)
  f.write((json.dumps(json_contents, sort_keys=True, indent=2, separators=(',', ': ')).decode('utf-8')))
  f.close


def do_request(action):
  # send a request to the server and return the response
  return requests.get(action)


def dynatrace_config_to_get(url_part, get_what, params="NOPARAMS", multipart="ISNT_MULTIPART"):
  # construct the url, send the request to the server, and write out the response to file
  if "NOPARAMS" in params:
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_STRING+API_KEY
  else:
    action = DYNATRACE_URL+ENVIRONMENT_ID+API_VERSION+url_part+API_STRING+API_KEY+params
  filename = get_what + ".json"
  server_response = do_request(action)
  print action + "\n"
  write_file(filename, server_response.content.decode('utf-8'))
  if "IS_MULTIPART" in multipart:
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
      dynatrace_config_to_get(new_url_part, new_get_what)


def get_config(config_file_name):
  # read in the config file and pull it into files ready to commit to a repo
  action_name = action_params = action_url = action_multipart = ""
  with open(config_file_name, 'r') as f:
    try:
      docs = yaml.load_all(f, Loader=yaml.FullLoader)
      for doc in docs:
        for k,v in doc.items():
          if "name" in k:
            action_name = v
          if "url" in k:
            action_url = v
          if "params" in k:
            action_params = v
          if "multipart" in k:
            action_multipart = v
        dynatrace_config_to_get(action_url, action_name, action_params, action_multipart)
    except yaml.YAMLError as exc:
      print(exc)


get_config(CONFIG_FILE)
