from . import main
import json
import requests
from flask import  g, jsonify, request, redirect, url_for, render_template

from functools import wraps


import logging

logger = logging.getLogger(__name__)


# app.config['LDAP_HOST'] = '172.16.19.20'
# app.config['LDAP_BASE_DN'] = 'CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_USERNAME'] = 'CN=Administrator,CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_PASSWORD'] = 'Xanadu@@12345'

"CN=Tarun Gupta,OU=Delhi AISGlass,OU=AIS Users,DC=asahiindia,DC=com"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('main.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
# @ldap.basic_auth_required
# @ldap.login_required
@login_required
def index():
    # username = session['username']
    # user_id_list = username.split("@")
    # user_id = user_id_list[0]
    # return 'Successfully logged in!'##Render template
    return render_template("new_index.html", user=1)



@main.route("/rasa/api/v1", methods=["POST"])
def rasa_api_hit():
    user_id = request.json.get('user_id')
    message = request.json.get('message')
    url = 'http://localhost:5005/webhooks/rest/webhook'  # rasa url
    payload = {
        'message': message,
        'sender': user_id
    }

    rasa_response = requests.post(url=url, data=json.dumps(payload))


    response = jsonify({"response": rasa_response.json()})
    return response


