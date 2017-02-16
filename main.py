import os
import os.path
import sys
from flask import Flask
from flask import render_template
from flask import request, url_for, make_response
import json
import logging
import MySQLdb
import dbconnect as db
import kras
import competencies as com
import apiai
import actions

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main_page():

	#CLIENT_ACCESS_TOKEN = "6d2145bdf1b4463c86d5c6bcc2f05b9c"
	CLIENT_ACCESS_TOKEN = "2f083c3517594ea093d1065014c13f11"

	if request.method == 'GET':
		
		return render_template("index.html")	

		#input_text = request.form['input_text'
	elif request.method == 'POST':
		#return request.form['message']
		sessionID = request.form['sessionID']
		ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
		req = ai.text_request()
		req.session_id = sessionID
		req.query = request.form['message']
		res = req.getresponse()
		response_message = res.read()
		response_message = json.loads(response_message)

		if response_message["result"]['parameters'].has_key('result') :
			return str(response_message["result"]['parameters']['result'])
		else:
			return response_message["result"]['fulfillment']['speech']
	
@app.route("/KRA", methods=['POST'])
def kra():
	logging.info("inside KRA")
	
	dbconnect = db.connect_to_cloudsql()

	if request.method == 'POST':
	
		logging.info("inside POST")
		req = request.get_json(silent=True, force=True)

		logging.info(type(req) )
		logging.info(req)

		parameters = req['result']['parameters']
		action = req['result']['action']

		webhook_res = actions.actions_handler[action](parameters, dbconnect)

		dbconnect.close()

		req = {
			"speech": webhook_res["speech"],
			"displayText": webhook_res["speech"],
			"data": {"speech": webhook_res["speech"] },
			"contextOut" : webhook_res["contextOut"]
		}
		
		req = json.dumps(req, indent=4)
		r = make_response(req)
		r.headers['Content-Type'] = 'application/json'
		return r



@app.route("/recognition", methods=['GET', 'POST'])
def recognition():
	return render_template("recognize.html")	

if __name__ == "__main__":
	app.run(debug=True,  port=int(8080))