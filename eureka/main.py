import json
from flask import Flask, request
from flask import Response
from watson_developer_cloud import PersonalityInsightsV3
import pymysql.cursors, os
from pymysql import escape_string as thwart
from credentials import *


personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    username=pi_username,
    password=pi_pass,
    url='https://gateway.watsonplatform.net/personality-insights/api'
)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='eureka',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


app = Flask(__name__)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/sendText', methods=['POST'])
def send_text():
    json_data = request.get_json(force=True)
    text = json_data['bodyOfText']
    username = json_data['username']
    res = personality_insights.profile(text, content_type='text/plain', raw_scores=True).get_result()
    output = {}
    for trait in res['personality']:
        output[trait['name']] = round(float(trait['percentile']), 2)
    json_output = json.dumps(output, indent=4)
    # store json output to db for later retrieval
    with connection.cursor() as cur:
		cur.execute("INSERT INTO records (username, traits) VALUES (%s,%s)", (thwart(username), thwart(json_output)))

    connection.commit()
    return Response('{"status":"ok"}', status=200, mimetype='application/json')

@app.route('/api/allData', methods=['GET'])
def all_data():
    with connection.cursor() as cur:
		cur.execute("SELECT * FROM records LIMIT 10")
		records = cur.fetchall()

    connection.commit()
    output = list()
    for item in records:
        output.append(dict(item))
    json_output = json.dumps(output)
    return json_output
