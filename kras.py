import logging
import os
import MySQLdb

def checkUser(parameters, db):
	logging.info("Inside checkUser()")

	cursor = db.cursor()

	logging.info("cursor built")
	cursor.execute("SELECT * FROM UserMaster WHERE FirstName = '%s' AND LastName = '%s' AND EmpCode = '%s'" % (parameters['firstname'].title(), parameters['lastname'].title(), '{0:06}'.format(int(parameters['employeeId']))))

	logging.info("query executed")
	count = cursor.rowcount

	logging.info("rowcount fetched")
	logging.info("count: "+str(count))

	if count > 0:
		logging.info("returning True")
		return { "speech" : "Welcome "+parameters['firstname'].title()+" "+parameters['lastname'].title()+" <br>How may I help you?",
				"contextOut": [{"name":"showkra", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : '{0:06}'.format(int(parameters['employeeId'])) }}] }
	else :
		logging.info("returning False")

		return { "speech" : "The Employee ID does not match with the name entered. <BR><BR> Please enter the correct Employee ID & your full name",
						"contextOut": [{"name":"getname", "lifespan":555, "parameters":{}}] }


def getKras(employeeId, parameters, db):
	logging.info("Inside getKras()")

	cursor = db.cursor()	

	logging.info("cursor built")

	cursor.execute("SELECT K.EmpKRAID, K.KRATitle, K.Weight FROM EmployeeKRA K, UserMaster U WHERE U.EmpCode = '%s' AND K.AppraisalCycleID = 12 AND K.EmpID = U.UserID" % (str(employeeId)))

	count = cursor.rowcount

	if count < 1:
		#return "KRA is not set"
		return { "speech" : "Your KRAs is not set. <br>How may I help you?", 
				"contextOut": [{"name":"showkra", "lifespan":555, "parameters": parameters}] }

	else:
		results = cursor.fetchall()
		speech = "These are the KRA titles<br>\
					<table>\
						<tr>\
							<th>KRAID</th>\
							<th>Title</th>\
							<th>Weight</th>\
						</tr>"

		for row in results:

			speech = speech + "\
				<tr>\
					<td>"+str(row[0])+"</td>\
					<td>"+str(row[1])+"</td>\
					<td>"+str(row[2])+"</td>\
				</tr>"
				
		speech = speech + "</table><br>\
							Enter the KRAID whose details you want to see"
		
		return { "speech" : speech,
		"contextOut": [{"name":"get_kra_title", "lifespan":555, "parameters": parameters}]}

def getKraSubordinate(employeeId, subordinateId, parameters, db):
	cursor = db.cursor()	

	logging.info("cursor built")
	
	if subordinateId :
		cursor.execute("SELECT COUNT(*) FROM UserMaster U WHERE U.ReportingManagerID = '%d' AND U.EmpCode = '%s'" % ( int(employeeId), str(subordinateId) ))

		count = cursor.fetchone()

		if count[0] < 1:

			return { "speech" : "This employeee is not your subordiante. Please Enter the subordinateId correctly.",
						"contextOut": [{"name":"show_kra_sub", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : employeeId, "whose" : parameters['whose'] , "subordinateId" : ""}}] }

		else:
			employeeId = subordinateId

			cursor.execute("SELECT K.EmpKRAID, K.KRATitle, K.Weight FROM EmployeeKRA K, UserMaster U WHERE U.EmpCode = '%s' AND K.EmpID = U.UserID" % (str(employeeId)))

			count = cursor.rowcount

			if count < 1:
				#return "KRA is not set"
				del parameters["subordinateID"]

				return { "speech" : "KRAs for this subordinate is not set <br> How may I help you?", 
						"contextOut": [{"name":"showkra", "lifespan":555, "parameters" : parameters}] }

			else:
				results = cursor.fetchall()
				speech = "These are the KRA titles<br>\
							<table>\
								<tr>\
									<th>KRAID</th>\
									<th>Title</th>\
									<th>Weight</th>\
								</tr>"

				for row in results:

					speech = speech + "\
						<tr>\
							<td>"+str(row[0])+"</td>\
							<td>"+str(row[1])+"</td>\
							<td>"+str(row[2])+"</td>\
						</tr>"
						
				speech = speech + "</table><br>\
									Enter the KRAID whose details you want to see"
				
				return { "speech" : speech,
				"contextOut": [{"name":"get_kra_title", "lifespan":555, "parameters": parameters}]}


def getSubordinates(employeeId, parameters, db):
	logging.info("Inside getSubordinates()")

	cursor = db.cursor()	

	logging.info("cursor built")

	cursor.execute("SELECT EmpCode, FirstName, LastName FROM UserMaster U WHERE U.ReportingManagerID = '%d'" % ( int(employeeId) ))

	count = cursor.rowcount

	if count < 1:
		return { "speech" : "You dont have any subordinates",
		"contextOut": [{"name":"showkra", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'] , "whose" : "" } }] }
			
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
						

		return { "speech" : speech,
				"contextOut": [{"name":"show_kra_sub", "lifespan":555, "parameters": parameters }] }
			

def getKraTitleDetails(KRAID, choice, whose, parameters, db):
	logging.info("Inside getKraTitleDetails()")

	cursor = db.cursor()	

	logging.info("cursor built")
	logging.info("KRAID :" + str(KRAID))
	logging.info("choice :" + str(choice))
	logging.info("type of KRAID :" + str(type(KRAID)))

	if choice == "description":
		cursor.execute("SELECT Description FROM EmployeeKRA WHERE EmpKRAID = '%d'" % (int(KRAID)))
	
	elif choice == "ratings":
		query = "SELECT ARM.Rating FROM EmployeeKRA EK, EmployeeKRARatings EKR, AppraisalRatingMaster ARM WHERE EK.EmpKRAID = EKR.EmpKRAID AND EKR.RatingID = ARM.AppraisalRatingsID AND EK.EmpKRAID = '%d'" % (int(KRAID))
		cursor.execute(query)

	elif choice == "self comment" :
		query = "SELECT SelfComments FROM EmployeeKRASelfComments WHERE EmpKRAID = '%d'" % (int(KRAID))
		cursor.execute(query)

	elif choice == "manager comment":
		cursor.execute()
	

	count = cursor.rowcount

	if count < 1:
		speech = str(choice)+" is not available for this KRAID. Try some other KRAID"

		del parameters["KRAID"]
		del parameters["choice"]
		return { "speech" : speech, 
				"contextOut": [{"name":"show_kra_title", "lifespan":555, "parameters": parameters }] }
	else:
		results = cursor.fetchall()
		speech = "KRA "+choice.title()+" : <br> "

		for row in results:
			speech = speech + str(row[0])

		if whose == 'me' and choice == 'self comment':
			speech = speech + "<br><br>Do you want to update the "+str(choice)+"?"
			contextOut = [{"name":"yes_update", "lifespan":555, "parameters": parameters }, {"name":"no_update", "lifespan":555, "parameters": parameters }]

		elif whose == 'subordinate' and choice != 'self comment' :
			speech = speech + "<br><br>Do you want to update the "+str(choice)+"?"
			contextOut = [{"name":"yes_update", "lifespan":555, "parameters": parameters }, {"name":"no_update", "lifespan":555, "parameters": parameters }]

		else:
			speech = speech + "<br><br>Request completed. What more can I do for you?"
			contextOut = [{"name":"showkra", "lifespan":555, "parameters": { "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : '{0:06}'.format(int(parameters['employeeId'])) } }]


	logging.info(speech)

	return { "speech" : speech, 
				"contextOut": contextOut }

def getKraTitleDetailsAll(KRAID, whose, parameters, db):
	logging.info("Inside getKraTitleDetailsAll()")

	cursor1 = db.cursor()	
	cursor2 = db.cursor()	
	cursor3 = db.cursor()	

	logging.info("cursor built")
	logging.info("KRAID :" + str(KRAID))
	logging.info("type of KRAID :" + str(type(KRAID)))

	#description
	query1 = "SELECT Description FROM EmployeeKRA WHERE EmpKRAID = '%d'" % (int(KRAID))
	cursor1.execute(query1)
		
	count = cursor1.rowcount

	if count < 1:
		speech = "<b>Description:</b> <br> Description is not available for this KRAID"

	else:
		results = cursor1.fetchall()
		speech = "<b>Description:</b> <br> "

		for row in results:
			speech = speech + str(row[0])


	# "ratings"
	query2 = "SELECT ARM.Rating FROM EmployeeKRARatings EKR, AppraisalRatingMaster ARM WHERE EKR.RatingID = ARM.AppraisalRatingsID AND EKR.EmpKRAID = '%d'" % (int(KRAID))
	cursor2.execute(query2)

	count = cursor2.rowcount

	if count < 1:
		speech = speech + "<br><br><b>Ratings:</b> <br> No ratings are available for this KRAID"

	else:
		results = cursor2.fetchall()
		speech = speech + "<br><br><b>Ratings:</b> <br> "

		for row in results:
			speech = speech + str(row[0])


	#"self comment" :
	query3 = "SELECT SelfComments FROM EmployeeKRASelfComments WHERE EmpKRAID = '%d'" % (int(KRAID))
	cursor3.execute(query3)

	count = cursor3.rowcount

	if count < 1:
		speech = speech + "<br><br><b>Self Comments:</b> <br> Self comment is not available for this KRAID"

	else:
		results = cursor3.fetchall()
		speech = speech + "<br><br><b>Self Comments:</b> <br> "

		for row in results:
			speech = speech + str(row[0])


	logging.info(speech)

	return { "speech" : speech+"<br><br>Request completed.", 
				"contextOut": [{"name":"showkra", "lifespan":555, "parameters": { "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : '{0:06}'.format(int(parameters['employeeId'])) } }] }


def updateKRA(KRAID, choice, newValue, parameters, db):
	logging.info("Inside updateKRA()")

	cursor = db.cursor()	

	logging.info("cursor built")
	logging.info("KRAID :" + str(KRAID))
	logging.info("choice :" + str(choice))
	logging.info("type of KRAID :" + str(type(KRAID)))
	logging.info("newValue:"+ str(newValue))

	speech = None
	if choice == "description":	
		try:
			cursor.execute("UPDATE EmployeeKRA set Description = '%s' WHERE EmpKRAID = '%d'" % (str(newValue), int(KRAID)))
			db.commit()
		except :
			db.rollback()
			speech = "Unable to update the Description. Please try again later"
		
	elif choice == "ratings":
		try:
			query = "SELECT ARM.AppraisalRatingsID FROM EmployeeKRA EK, EmployeeKRARatings EKR, AppraisalRatingMaster ARM WHERE EK.EmpKRAID = EKR.EmpKRAID AND EKR.RatingID = ARM.AppraisalRatingsID AND EK.EmpKRAID = '%d'" % ( int(KRAID))
			cursor.execute(query)
			results = cursor.fetchone()
			logging.info("results :"+str(results))
			query2 = "UPDATE AppraisalRatingMaster set Rating = '%d' WHERE AppraisalRatingsID = '%d'" % (int(newValue),int(results[0]))
			cursor = db.cursor()
			cursor.execute(query2)
			db.commit()
		except:
			db.rollback()
			speech = "Unable to update the Rating. Please try again later"

	elif choice == "self comment" :
		try:
			query = "UPDATE EmployeeKRASelfComments SET SelfComments = '%s' WHERE EmpKRAID = '%d'" % (str(newValue), int(KRAID))
			cursor.execute(query)
			db.commit()
		except:
			db.rollback()
			speech = "Unable to update the Self Comments. Please try again later"

	elif choice == "manager comment":
		try:
			query = ""
			cursor.execute(query)
			db.commit()
		except:
			db.rollback()
			speech = "Unable to update the Manager's Comments. Please try again later"

	if not speech:
		speech = choice.title() + " updated successfully to "+str(newValue)+"<br> Request completed"

	return { "speech" : speech+"<br><br>How may I help you?",
			"contextOut" :[{"name":"showname", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'] }}] }
