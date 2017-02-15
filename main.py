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

		if action == 'getname': #case for authentication

			logging.info("inside getname")
			if kras.checkUser(parameters['firstname'].title(), parameters['lastname'].title(), '{0:06}'.format(int(parameters['employeeId'])), dbconnect) :
				logging.info("returning True")
				webhook_res = { "speech" : "Welcome "+parameters['firstname']+" "+parameters['lastname']+" <br>How may I help you?",
								"contextOut": [{"name":"showkra", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'] }}] }
			else:
				logging.info("returning False")

				webhook_res = { "speech" : "The Employee ID does not match with the name entered. <BR><BR> Please enter the correct Employee ID & your full name",
								"contextOut": [{"name":"getname", "lifespan":555, "parameters":{}}] }
			
		elif action == 'showkra': #case to show kra
			logging.info("inside showkra")

			if parameters['whose'].lower() == 'me':
				speech = kras.getKras('{0:06}'.format(int(parameters['employeeId'])),dbconnect)
				webhook_res = { "speech" : speech['speech'],
								"contextOut": [{"name":speech['contextOut'], "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'], "whose" : parameters['whose'] } }] }


			elif parameters['whose'].lower() == 'subordinate':
				speech = kras.getSubordinates('{0:06}'.format(int(parameters['employeeId'])), dbconnect)
				webhook_res = { "speech" : speech,
								"contextOut": [{"name":"show_kra_sub", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'], "whose" : parameters['whose'] } }] }

			else:
				webhook_res = { "speech" : "I didnt get that.. <BR> Please try entering correctly, Whose KRAs do you want to see? (yourself / subordinate)",
								"contextOut": [{"name":"showkra", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'] } }] }

		elif action == 'showkra_of_subordinate':
			speech = kras.getKras('{0:06}'.format(int(parameters['employeeId'])), dbconnect, '{0:06}'.format(int(parameters['subordinateId'])))

		elif action == "get_kra_title":
			speech = kras.getKraDescription(parameters['KRAID'],parameters['choice'].lower(), parameters['whose'].lower(), dbconnect)	

		elif action == "update_yes_kra" :
			speech = kras.updateKRA(parameters['KRAID'], parameters['choice'].lower(), parameters['newValue'], dbconnect)
		




		elif action == "show_competencies":
			logging.info("inside show_competencies")

			if parameters['whose'].lower() == 'me' or parameters['whose'].lower() == 'my' or parameters['whose'].lower() == 'myself' :
				speech = com.getCompetencies('{0:06}'.format(int(parameters['employeeId'])),dbconnect)

			elif parameters['whose'].lower() == 'subordinate' or parameters['whose'].lower() == 'subordinates':
				speech = com.getSubordinates('{0:06}'.format(int(parameters['employeeId'])), dbconnect)
			else:
				speech = "I didnt get that.."

		elif action == "show_competencies_of_subordinate":
			
			speech = com.getCompetencies('{0:06}'.format(int(parameters['employeeId'])), dbconnect, '{0:06}'.format(int(parameters['subordinateId'])))

		elif action == "get_competencies_details":
			speech = com.getCompetencies_details(parameters['EmpCompetencyID'], dbconnect)

		else:
			logging.info("returning default")
			speech = "Hi, how may I help you"

		dbconnect.close()

		if webhook_res:
			req = {
					"speech": webhook_res["speech"],
					"displayText": webhook_res["speech"],
					"data": {"speech": webhook_res["speech"] },
					"contextOut" : webhook_res["contextOut"]
				}
		else :
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