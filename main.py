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

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main_page():

	if request.method == 'GET':
		
		return render_template("index.html")	

		#input_text = request.form['input_text'
	
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
		for p in parameters:
			logging.info(p)
			logging.info(parameters[p])

		# logging.info("parameters : "+ parameters)
		if parameters['action'] == 'getname':

			logging.info("inside action")
			if db.checkUser(parameters['firstname'], parameters['lastname'], parameters['employeeId'], dbconnect) :
				logging.info("returning True")
				return "Welcome "#+parameters['firstname']+" "+parameters['lastname']
			else:
				logging.info("returning False")

				req = {
					"speech": "Failed to authenticate",
					"displayText": "Failed to authenticate",
					"data": {"speech": "Failed to authenticate"},
					}
					
				req = json.dumps(req, indent=4)
				r = make_response(req)
				r.headers['Content-Type'] = 'application/json'
				return r
		else:
			logging.info("returning default")
			return "default"



if __name__ == "__main__":
	app.run(debug=True,  port=int(8080))