import os
import os.path
import sys
from flask import Flask
from flask import render_template
from flask import request, url_for
import json

app = Flask(__name__, static_url_path='/static')

CLIENT_ACCESS_TOKEN = '2e305571959847228c0c4a5d9a33b4c6'

@app.route("/", methods=['GET', 'POST'])
def main_page():

	if request.method == 'GET':
		
		return render_template("index.html")	

		#input_text = request.form['input_text'
	
if __name__ == "__main__":
	app.run(debug=True,  port=int(8080))