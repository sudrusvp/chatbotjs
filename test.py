
from flask import Flask
from flask import render_template
from flask import request, url_for

import MySQLdb


app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return "hello world"


if __name__ == "__main__":
    app.run(debug=True,  port=int(8080))