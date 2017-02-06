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

	cursor = db.cursor()

	logging.info("cursor built")
	cursor.execute("SELECT * FROM UserMaster WHERE FirstName = '%s' AND LastName = '%s' AND EmpCode = '%s'" % (firstname, lastname, str(employeeId)))

	logging.info("query executed")
	count = cursor.rowcount

	logging.info("rowcount fetched")
	logging.info("count: "+str(count))

	if count > 0:
		return True
	else :
		return False