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
import apiai

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main_page():

	CLIENT_ACCESS_TOKEN = "6d2145bdf1b4463c86d5c6bcc2f05b9c"

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

		if action == 'getname': #case for authentication

			logging.info("inside getname")
			if db.checkUser(parameters['firstname'].title(), parameters['lastname'].title(), parameters['employeeId'], dbconnect) :
				logging.info("returning True")
				speech = "Welcome "+parameters['firstname']+" "+parameters['lastname']+" <br>How may I help you?"
			else:
				logging.info("returning False")

				speech = "Failed to authenticate!!! <br> Please re-enter your fullname and employee ID"
			
		elif action == 'showkra': #case to show kra
			logging.info("inside showkra")

			if parameters['whose'].lower() == 'me' or parameters['whose'].lower() == 'my' or parameters['whose'].lower() == 'myself' :
				speech = db.getKras(parameters['employeeId'], dbconnect)

			elif parameters['whose'].lower() == 'subordinate':
				speech = db.getSubordinates(parameters['employeeId'], dbconnect)
			else:
				speech = "I didnt get that.."
		elif action == 'showkra_of_subordinate':
			speech = db.getKras(parameters['subordinateId'], dbconnect)

		elif action == "get_kra_title":

			speech = db.getKraDescription(parameters['KRAID'],parameters['choice'].lower(), dbconnect)	

		else:
			logging.info("returning default")
			speech = "Hi, how may I help you"

		dbconnect.close()

		req = {
				"speech": speech,
				"displayText": speech,
				"data": {"speech": speech},
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