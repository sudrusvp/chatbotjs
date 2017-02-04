import os
import os.path
import sys
from flask import Flask
from flask import render_template
from flask import request, url_for
import json
import apiai

app = Flask(__name__, static_url_path='/static')

CLIENT_ACCESS_TOKEN = '2e305571959847228c0c4a5d9a33b4c6'

@app.route("/", methods=['GET', 'POST'])
def main_page():

	if request.method == 'GET':
		
		return render_template("index.html")	

		#input_text = request.form['input_text']

	elif request.method == 'POST':
		#return request.form['message']
		ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
		req = ai.text_request()
		req.session_id = "session11"
		req.query = request.form['message']
		res = req.getresponse()
		response_message = res.read()
		response_message = json.loads(response_message)
		return response_message["result"]['fulfillment']['speech']
	
if __name__ == "__main__":
	app.run(debug=True,  port=int(8080))