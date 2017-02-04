import os
import os.path
import sys
from flask import Flask
from flask import render_template
from flask import request, url_for
import json
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

	if request.method == 'POST':
		parameters = request.form['result']['parameters']

		if parameters['action'] == 'getname':

			if db.checkUser(parameters['firstname'], parameters['lastname'], parameters['employeeId']) :
				return "Welcome"
			else:
				return "Failed to authenticate"
		else:
			return "default"



if __name__ == "__main__":
	app.run(debug=True,  port=int(8080))