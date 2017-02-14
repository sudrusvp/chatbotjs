import logging
import os
import MySQLdb

def getCompetencies(employeeId, db, subordinateId=None):
	logging.info("Inside getCompetencies()")

	cursor = db.cursor()	

	logging.info("cursor built")

	if subordinateId :
		cursor.execute("SELECT COUNT(*) FROM UserMaster U WHERE U.ReportingManagerID = '%d' AND U.EmpCode = '%s'" % ( int(employeeId), str(subordinateId) ))

		count = cursor.fetchone()

		if count[0] < 1:
			return "This employeee is not your subordiante"
		else:
			employeeId = subordinateId


	cursor1 = db.cursor()	
	cursor2 = db.cursor()	
	cursor3 = db.cursor()

	cursor1.execute("SELECT C.CompetencyID, C.DesiredLevelID, C.EmpCompetencyID FROM EmployeeCompetency C, UserMaster U WHERE U.EmpCode = '%s' AND C.EmpID = U.UserID" % (str(employeeId)))

	count = cursor1.rowcount

	if count < 1:
		return "Competency is not set"
	else:
		result1 = cursor1.fetchall()
		speech = "These are the competencies<br>\
					<table>\
						<tr>\
							<th>ID</th>\
							<th>Title</th>\
							<th>Desired Level</th>\
							<th>Rating</th>\
						</tr>"

		for row in result1:

			cursor2.execute("SELECT Title FROM CustomerCompetencyMaster WHERE CompetencyID = '%d'" % (int(row[0])))

			query = "SELECT ARM.Rating FROM EmployeeCompetency EC, EmployeeCompetencyRatings ECR, AppraisalRatingMaster ARM WHERE EC.EmpCompetencyID = ECR.EmpCompetencyID AND ECR.RatingID = ARM.AppraisalRatingsID AND EC.EmpCompetencyID = '%d'" % (int(row[2]))
			cursor3.execute(query)

			result2 = cursor2.fetchone()
			result3 = cursor3.fetchone()
			if not result3:
				result3[0] = "NOT SET"

			speech = speech + "\
				<tr>\
					<td>"+str(int(row[0]))+"</td>\
					<td>"+str(result2[0])+"</td>\
					<td>Level "+str(row[1])+"</td>\
					<td>"+str(result3[0])+"</td>\
				</tr>"
				
		speech = speech + "</table>"

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
							Enter the Employee code of the subordinate, whose competencies you want to see"
									
		return speech
