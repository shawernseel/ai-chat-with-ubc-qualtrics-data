from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import urllib
import sys
import requests
import os
import simplejson as json
from dotenv import load_dotenv
load_dotenv()

survey_id = os.environ['SURVEY_ID']
api_key = os.environ['API_KEY']
data_center = os.environ['DATA_CENTER']

headers = {
    "content-type": "application/json",
    "x-api-token": api_key,
   }
url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(data_center,survey_id,)
rsp = requests.get(url, headers=headers)
print(rsp.json())

#webhook handles qualtrics updating data
'''
def getReponse(d,dataCenter,apiToken):
    responseId = d['ResponseID']
    surveyId = d['SurveyID']

    headers = {
        "content-type": "application/json",
        "x-api-token": api_key,
       }

    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(dataCenter,surveyId,responseId)

    
    rsp = requests.get(url, headers=headers)
    print(rsp.json())


def parsey(c):
    x=c.decode().split("&")
    d = {}
    for i in x:
        a,b = i.split("=")
        d[a] = b

    d['CompletedDate'] = urllib.parse.unquote(d['CompletedDate'])

    return d

class Handler(BaseHTTPRequestHandler):

  # GET
  def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        d = parsey(post_data)

        try:
           apiToken = api_key
           dataCenter = data_center
        except KeyError:
            print("set environment variables APIKEY and DATACENTER")
            sys.exit(2)

        getReponse(d,dataCenter,apiToken)
 
def run():

  print('starting server...')
  server_address = ('127.0.0.1', 8080)
 
  httpd = HTTPServer(server_address, Handler)
  print('running server...')
  httpd.serve_forever()
 

try: 
    run()
except KeyboardInterrupt:
    sys.exit(0)
'''