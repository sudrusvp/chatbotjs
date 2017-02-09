import logging
import os
import MySQLdb

def connect_to_cloudsql():

	# These environment variables are configured in app.yaml.
	INSTANCE_CONNECTION_NAME = os.environ.get('INSTANCE_CONNECTION_NAME')
	CLOUDSQL_USER = os.environ.get('MYSQL_USER')
	CLOUDSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
	CLOUDSQL_DB = os.environ.get('MYSQL_DATABASE')
	
	cloudsql_unix_socket = os.path.join('/cloudsql', INSTANCE_CONNECTION_NAME)

	db = MySQLdb.connect(
		unix_socket=cloudsql_unix_socket,
		user=CLOUDSQL_USER,
		passwd=CLOUDSQL_PASSWORD,
		db=CLOUDSQL_DB)

	logging.info("connected to db")
	return db


def checkUser(firstname, lastname, employeeId, db):
	logging.info("Inside checkUser()")

	cursor = db.cursor()

	logging.info("cursor built")
	cursor.execute("SELECT * FROM UserMaster WHERE FirstName = '%s' AND LastName = '%s' AND EmpCode = '%s'" % (firstname, lastname, employeeId))

	logging.info("query executed")
	count = cursor.rowcount

	logging.info("rowcount fetched")
	logging.info("count: "+str(count))

	if count > 0:
		return True
	else :
		return False


def getKras(employeeId, db):
	logging.info("Inside getKras()")

	cursor = db.cursor()	

	logging.info("cursor built")
	cursor.execute("SELECT K.KRATitle, K.Weight FROM EmployeeKRA K, UserMaster U WHERE U.EmpCode = '%s' AND K.EmpID = U.UserID" % (employeeId))

	count = cursor.rowcount

	if count < 1:
		return "You dont have any KRA set"
	else:
		results = cursor.fetchall()
		speech = "These are the KRA titles<br>\
					<table>\
						<tr>\
							<th>Title</th>\
							<th>Weight</th>\
						</tr>"

		for row in results:

			speech = speech + "\
				<tr>\
					<td>"+str(row[0])+"</td>\
					<td>"+str(row[0])+"</td>\
				</tr>"
				
		speech = speech + "</table><br>"

		return speech


def getSubordinates(employeeId, db):
	logging.info("Inside getSubordinates()")

	cursor = db.cursor()	

	logging.info("cursor built")

	cursor.execute("SELECT EmpCode, FirstName, LastName FROM UserMaster U WHERE U.ReportingManagerID = '%d'" % ( int(employeeId) ))

	count = cursor.rowcount

	if count < 1:
		return "You dont have any subordinates"
	else:
		results = cursor.fetchall()
		speech = "These are your subordinates: <br>\
					<table>"
		for row in results:
			speech = speech + "<tr>\
								<td>"+str(row[0])+"</td>\
								<td>"+str(row[1])+" "+str(row[2])+"</td>\
							</tr>"

		speech = speech + "</table>\
							Enter the Employee code of the subordinate, whose KRA you want to see"
									
		return speech


