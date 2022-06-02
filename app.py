import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import json

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "4dFMp5kVdPug4PjkUEeJLPpRVkvmbdBlXjm9q2-MqCVE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
# NOTE: manually define and pass the array(s) of values to be scored in the next line
# payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

app = Flask(__name__)
model= pickle.load(open('mining.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    avg_air_flow_267 = request.form["avg_air_flow_267"]
    avg_float_level_47 = request.form["avg_float_level_47"]
    Iron_Feed= request.form["% Iron Feed"]
    Amina_Flow= request.form["Amina Flow"]
    Ore_Pulp_pH= request.form["Ore Pulp pH"]
    Ore_Pulp_Density = request.form["Ore Pulp Density"]
    t = [[int(avg_air_flow_267),int(avg_float_level_47),int(Iron_Feed),int(Amina_Flow ),int(Ore_Pulp_pH ),int(Ore_Pulp_Density)]]
    payload_scoring = {"input_data": [{"fields": [["avg_air_flow_267", "avg_float_level_47", "Iron Feed", "Amina Flow", "Ore Pulp pH", "Ore Pulp Density"]], "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/3f2a6d50-aa9d-42e9-838e-3e20afb356e3/predictions?version=2022-03-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    
    x_test = [[x for x in request.form.values()]]
    prediction = model.predict(x_test)
    pred=prediction[0]
    print(prediction)
    return render_template('index.html', prediction_text='Predicted Quality:{}'.format(pred))

@app.route('/about')
def about():
    return  render_template("about.html")
    

if __name__ == "__main__":
    app.run(debug=True)

