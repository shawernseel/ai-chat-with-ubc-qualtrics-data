#qualtrics api doccumentation: https://api.qualtrics.com/
# https://api.qualtrics.com/5d17de1a27084-example-use-cases-walkthrough
# https://api.qualtrics.com/5e86e383167d5-getting-survey-responses-via-the-new-export-ap-is

import requests
import zipfile
import io
import os
import datetime

from dotenv import load_dotenv, dotenv_values
load_dotenv()

dir_save_survey = os.getenv("dir_save_survey")
survey_id = os.getenv("survey_id")

path_to_local_folder = os.getenv("path_to_local_folder")

#User Parameters
api_token: str = os.getenv("api_token")
file_format = "json"
data_center = os.getenv("data_center")

#Static Parameters
request_check_progress = 0.0
progressStatus = "in progress"
base_url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(data_center, survey_id)
headers = {
    "content-type": "application/json",
    "x-api-token": api_token,
}

# Step 1: Creating Data Export
downloadRequestUrl = base_url
downloadRequestPayload = '{"format":"' + file_format + '","compress":"false"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
progressId = downloadRequestResponse.json()["result"]["progressId"]
print(downloadRequestResponse.text)

'''
# Step 2: Checking on Data Export Progress and waiting until export is ready
while progressStatus != "complete" and progressStatus != "failed":
    print ("progressStatus=", progressStatus)
    requestCheckUrl = base_url + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    print("Download is " + str(requestCheckProgress) + " complete")
    progressStatus = requestCheckResponse.json()["result"]["status"]

#step 2.1: Check for error
if progressStatus == "failed":
    raise Exception("export failed")


fileId = requestCheckResponse.json()["result"]["fileId"]

# Step 3: Downloading file
requestDownloadUrl = base_url + fileId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)
print(requestDownload.content)
print("!")

# Step 4: Unzipping the file
unique_folder_name = os.path.join(path_to_local_folder, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(path_to_local_folder, exist_ok=True)
with zipfile.ZipFile(io.BytesIO(requestDownload.content)) as zip_ref:
    zip_ref.extractall(unique_folder_name)
print(f'Complete. Files extracted to {unique_folder_name}')
'''
