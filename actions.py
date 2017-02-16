
import kras
import competencies as com

def getname(parameters, dbconnect):
	logging.info("inside getname")
	return kras.checkUser(parameters, dbconnect)

def showkra( parameters, dbconnect):
	logging.info("inside showkra")

	if parameters['whose'].lower() == 'me':
		webhook_res = kras.getKras('{0:06}'.format(int(parameters['employeeId'])), parameters, dbconnect)

	elif parameters['whose'].lower() == 'subordinate':
		webhook_res = kras.getSubordinates('{0:06}'.format(int(parameters['employeeId'])),parameters dbconnect)
	
	else:
		webhook_res = { "speech" : "I didnt get that.. <BR> Please try entering correctly, Whose KRAs do you want to see? (yourself / subordinate)",
						"contextOut": [{"name":"showkra", "lifespan":555, "parameters":{ "firstname": parameters['firstname'], "lastname" : parameters['lastname'], "employeeId" : parameters['employeeId'] } }] }

	return webhook_res


def showkra_of_subordinate( parameters, dbconnect):
	return kras.getKraSubordinate('{0:06}'.format(int(parameters['employeeId'])), '{0:06}'.format(int(parameters['subordinateId'])), parameters, dbconnect)

def get_kra_title( parameters, dbconnect):
	return kras.getKraTitleDetails(parameters['KRAID'],parameters['choice'].lower(), parameters['whose'].lower(), parameters, dbconnect)	

def update_yes_kra( parameters, dbconnect):
	webhook_res = kras.updateKRA(parameters['KRAID'], parameters['choice'].lower(), parameters['newValue'], dbconnect)
	return webhook_res

def show_competencies( parameters, dbconnect):
	logging.info("inside show_competencies")

	if parameters['whose'].lower() == 'me' or parameters['whose'].lower() == 'my' or parameters['whose'].lower() == 'myself' :
		speech = com.getCompetencies('{0:06}'.format(int(parameters['employeeId'])),dbconnect)

	elif parameters['whose'].lower() == 'subordinate' or parameters['whose'].lower() == 'subordinates':
		speech = com.getSubordinates('{0:06}'.format(int(parameters['employeeId'])), dbconnect)
	else:
		speech = "I didnt get that.."

	return webhook_res

def show_competencies_of_subordinate( parameters, dbconnect):
	webhook_res = com.getCompetencies('{0:06}'.format(int(parameters['employeeId'])), dbconnect, '{0:06}'.format(int(parameters['subordinateId'])))

	return webhook_res

def get_competencies_details( parameters, dbconnect):
	webhook_res = com.getCompetencies_details(parameters['EmpCompetencyID'], dbconnect)

	return webhook_res

actions_handler = {
	"getname" : getname,
	"showkra" : showkra,
	"showkra_of_subordinate" : showkra_of_subordinate,
	"get_kra_title" : get_kra_title,
	"update_yes_kra" : update_yes_kra,
	"show_competencies" : show_competencies,
	"show_competencies_of_subordinate" : show_competencies_of_subordinate,
	"get_competencies_details" : get_competencies_details, 
}
