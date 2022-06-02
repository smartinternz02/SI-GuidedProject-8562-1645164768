import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template
import json


import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "4dFMp5kVdPug4PjkUEeJLPpRVkvmbdBlXjm9q2-MqCVE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line


response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/fa77d021-01ee-492f-afc0-acf84ba1314e/predictions?version=2022-03-25', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())


