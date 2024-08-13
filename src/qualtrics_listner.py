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

print(survey_id, api_key, data_center)