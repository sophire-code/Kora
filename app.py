#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "getTotalNumber":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    field = parameters.get("field")
    if field is None:
        return {}
    print("field:")
    print(field)
    url = "http://koratest.sophire.org/wp-json/wp/v2/" + field
    results = urllib.urlopen(url).read()
    data = json.loads(results)
    print(len(data))
    res = makeWebhookResult(field, len(data))
    return res

def makeWebhookResult(field, length):
    speech = "The total number of \"" + field + "\" is  " + str(length)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "api-ai-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print "Starting app on port %d" % port
app.run(debug=False, port=port, host='0.0.0.0')