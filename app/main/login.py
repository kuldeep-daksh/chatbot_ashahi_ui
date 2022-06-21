
from . import main

from flask import  g, request, session, redirect, url_for, render_template, flash
import ldap
from functools import wraps
import logging
logger = logging.getLogger(__name__)


# app.config['LDAP_HOST'] = '172.16.19.20'
# app.config['LDAP_BASE_DN'] = 'CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_USERNAME'] = 'CN=Administrator,CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_PASSWORD'] = 'Xanadu@@12345'

username = f"CN={username},OU=Delhi AISGlass,OU=AIS Users,DC=asahiindia,DC=com"
password = "tasty@lemon09"

@main.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if is_user_authenticated():
        return render_template('new_index.html')
    if request.method == 'POST':
        username = request.form['userid']
        password = request.form['password']
        if username and password:
            try:
                user_exist = is_user_exist(
                    "80.0.0.108", username, password)
                # user_exist = is_user_exist_test(
                #     "172.16.19.20", username, password)
                if user_exist:
                    authenticate_user(username)
                    return redirect(url_for('main.index'))
                else:
                    error = 'Wrong email or password'
                    return render_template("login.html", error=error)
            except Exception as e:
                error = e
                return render_template("login.html", error=error)
    return render_template('login.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@main.before_app_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.user = None
        g.count = None
    else:
        g.user = username


def authenticate_user(username):
    session.clear()
    session['signed_in'] = True
    session['username'] = username


def is_user_exist(address, username, password):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    print("gfdknkgnhkgfnhgkhn")
    return conn.simple_bind_s(username, password)


# def is_user_exist_test(address, username, password):
#     userid = "13666"
#     pwd = "12345"
#     if userid == username and password == pwd:
#         return True
#     else:
#         return False


def is_user_authenticated():
    load_logged_in_user()
    if g.user:
        return True
    else:
        return False
