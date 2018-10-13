import json
from flask import Flask, request
from watson_developer_cloud import PersonalityInsightsV3

from credentials import *


personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    username=pi_username,
    password=pi_pass,
    url='https://gateway.watsonplatform.net/personality-insights/api'
)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/sendText', methods=['POST'])
def send_text():
    text = request.form['bodyOfText']
    # save to db with corresponding user
    username = request.form['username']
    # send results back to user
    res = personality_insights.profile(
        text, content_type='text/plain', raw_scores=True
        ).get_result()
    output = {}
    for trait in res['personality']:
        output[trait['name']] = round(float(trait['percentile']), 2)
    # now send this back?
    return json.dumps(output)
    # Or just return a success or failure message, and send analysis via a
    # different endpoint?