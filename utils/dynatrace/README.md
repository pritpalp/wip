## get_dynatrace_config.py

This script will pull the Dynatrace config from the server.

### Requirements
The following environment variables need to be set before the script is run:

```bash
export API_KEY=xxx
export DYNATRACE_URL=xxx
export ENVIRONMENT_ID=xxx
export DYNATRACE_CONF_PATH=xxx
export DYNATRACE_CONFIG_FILE=xxx
```

**ENVIRONMENT_ID**, **DYNATRACE_URL** and **API_KEY** can be changed to reflect the environment that we want to pull the info from

**DYNATRACE_CONF_PATH** is the path that you want to save the json files out to

**DYNATRACE_CONFIG_FILE** is the path to the file containing the config for the various parts of dyanatrace config we want to grab

**API_KEY** needs to have ***Read Configuration*** permission

The best way to set these values is to put them into a file, *env.sh*
This file will not be added to the repo...

The **python package *requests* and *yaml*** are required to run the script:

```bash
$ pip install --user requests
$ pip install --user yaml
```

### DYNATRACE_CONFIG_FILE

This is a yaml file containing the information that is required to pull info from the API. Structured as follows with the "---" delimiting the records:

```yaml
---
name:           xxx
dynatrace_url:  xxx
params:         xxx
multipart:      xxx
---
```

### Run
To run the script:

```bash
$ python get_dynatrace_config.py
```

This will output a series of json files containing Dynatrace config
