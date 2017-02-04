
import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '2e305571959847228c0c4a5d9a33b4c6'

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.session_id = "session11"

    request.query = "Hello"

    response = request.getresponse()

    result = response.read()

    print "result : ",result
    print "\ntype of : ",type(result)
    result = json.loads(result);
    print "\nresult.result : ",result["result"]['fulfillment']['speech']


if __name__ == '__main__':
    main()