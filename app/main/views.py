from flask import Flask

from . import main


from flask import Flask, g, request, session, redirect, url_for, render_template, flash

import ldap
from functools import wraps


import logging

logger = logging.getLogger(__name__)


# app.config['LDAP_HOST'] = '172.16.19.20'
# app.config['LDAP_BASE_DN'] = 'CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_USERNAME'] = 'CN=Administrator,CN=Users,DC=tcplcoe,DC=com'
# app.config['LDAP_PASSWORD'] = 'Xanadu@@12345'



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('main.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# @main.before_request
# def before_request():
#     logger.info(" i am here before the request proceed")
#     g.user = None
#     logger.info("--->", dir(session))
#     for key, value in session.items():
#         logger.info("key", key, value)
#     if 'user_id' in session:
#         # This is where you'd query your database to get the user info.
#         g.user = {}
#         # Create a global with the LDAP groups the user is a member of.
#         g.ldap_groups = ldap.get_user_groups(user=session['user_id'])
#     logger.info("g.ldap_groups", dir(ldap))


@main.route('/')
# @ldap.basic_auth_required
# @ldap.login_required
# @login_required
def index():
    logger.info("i am in the index function ----------------------------------------------------------")
    # username = session['username']
    # user_id_list = username.split("@")
    # user_id = user_id_list[0]
    # return 'Successfully logged in!'##Render template
    return render_template("new_index.html", user=1)


@main.route('/new')
# @ldap.basic_auth_required
# @ldap.login_required
# @login_required
def new_index():
    logger.info("i am in the index function")
    # username = session['username']
    # user_id_list = username.split("@")
    # user_id = user_id_list[0]
    # return 'Successfully logged in!'##Render template
    return render_template("new_index.html", user=1)


# @main.route('/route', methods=['GET', 'POST'])
# @ldap.basic_auth_required
# # @ldap.login_required
# def inde():
#     logger.info("i am in the index function")
#     # logger.info("g.user", g.ldap_username)
#     global user
#     user = "user"
#     # return 'Successfully logged in!'##Render template
#     return render_template("index.html", user="user")


# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     logger.info("In login")
#     if g.user:
#         logger.info("g.user", g.user)
#         return redirect(url_for('index'))
#
#     if request.method == 'POST':
#         logger.info("i am in the login function -- -------------------------")
#
#         logger.info("request.method ", request.method)
#         user = request.form['user']
#         logger.info(user)
#         passwd = request.form['passwd']
#         logger.info(passwd)
#         test = ldap.bind_user(user, passwd)
#         logger.info(test)
#         if test is None or passwd == '':
#             return 'Invalid credentials'
#         else:
#             session['user_id'] = request.form['user']
#             logger.info("session['user_id']")
#             return redirect('/')
#     # return "Success"
#     logger.info("session['user_id']")
#     return redirect('/')

#
# @main.route('/group')
# @ldap.group_required(groups=['Users'])
# def group():
#     return 'Group restricted page'


@main.before_request
def before_request():
    g.user = session.get('username')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# @main.route('/getUserId')
# def get_user_id():
#     return user


@main.route('/login', methods=('GET', 'POST'))
def login():
    if is_user_authenticated():
        return render_template('index.html')
    if request.method == 'POST':
        logger.info("mmbbgjdfbgjdbgfhjgfjdf")
        username = request.form['usrnm']
        logger.info(username)
        password = request.form['psw']
        logger.info(password)
        if username and password:
            try:
                user_exist = is_user_exist("localhost:5055", username, password)
                if user_exist:
                    authenticate_user(username)
                    return redirect(url_for('index'))
                else:
                    flash('Wrong email or password')
                    return render_template("login.html")
            except:
                flash('Wrong email or password')
                return render_template("login.html")
    return render_template('login.html')


def is_user_authenticated():
    load_logged_in_user()
    if g.user:
        return True
    else:
        return False


# @bp.before_app_request
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
    return conn.simple_bind_s(username, password)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


