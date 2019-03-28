## get_dynatrace_config.py

This script will pull the Dynatrace config from the server.

### Requirements
The following environment variables need to be set before the script is run:

```bash
export API_KEY=xxx
export DYNATRACE_URL=xxx
export ENVIRONMENT_ID=xxx
export DYNATRACE_CONF_PATH=xxx
```

**ENVIRONMENT_ID**, **DYNATRACE_URL** and **API_KEY** can be changed to reflect the environment that we want to pull the info from

**DYNATRACE_CONF_PATH** is the path that you want to save the json files out to

**API_KEY** needs to have ***Read Configuration*** permission

The best way to set these values is to put them into a file, *env.sh*
This file will not be added to the repo...

The **python package *requests*** is required to run the script:

```bash
$ pip install --user requests
```

### Run
To run the script:

```bash
$ python get_dynatrace_config.py
```

This will output a series of json files containing Dynatrace config
