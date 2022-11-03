import requests
import argparse
import os

# add argument for reportname
parser = argparse.ArgumentParser()
parser.add_argument('--reportname', default='myreport')
parser.add_argument('--reportdir', default=os.getcwd())
parser.add_argument('--sites', default='https://mywebsite.com')
parser.add_argument('--zapkey', default='randomAPIKeyHere')
args = parser.parse_args()

# This is the command we want to run once ZAP is running on daemon mode
# http://localhost:8080/JSON/reports/action/generate/?apikey=randomAPIKeyHere&title=test&template=traditional-html&theme=&description=&contexts=&sites=https%3A%2F%2Fmywebsite.com&sections=&includedConfidences=&includedRisks=&reportFileName=&reportFileNamePattern=&reportDir=&display=

zapAddress = "http://localhost:8080/JSON/reports/action/generate/"
zapAPIKey = args.zapkey
title = "My OWASP ZAP Report"
template = "traditional-html"
sites = args.sites
reportFileName = args.reportname
reportDir = args.reportdir

try:
   # check that we get a response from ZAP
   response = requests.get("http://localhost:8080", stream=False, timeout=None)
   print(response.status_code)
   query = {'apikey':zapAPIKey,'title':title,'template':template,'sites':sites,'reportFileName':reportFileName,'reportDir':reportDir}
   headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
   }
   print(query)
   print(zapAddress)
   print(sites)
   print(reportFileName)
   print(reportDir)
   response = requests.get(zapAddress, query, headers=headers, stream=False, timeout=None)
   print(response.status_code)
   print(response.json())
except requests.exceptions.HTTPError as errh:
    print(errh)
except requests.exceptions.ConnectionError as errc:
    print(errc)
except requests.exceptions.Timeout as errt:
    print(errt)
except requests.exceptions.RequestException as err:
    print(err)