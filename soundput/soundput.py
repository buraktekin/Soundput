# Burak Tekin
# Istanbul Bilgi University
#Department of Computer Science
#Sources:
#     *http://flask.pocoo.org/docs/tutorial/#tutorial)
#     *put.io API
#     *MongoDB
#-----------------------------------------------------------------------------
import json, pymongo, putio
from flask import Flask, g, render_template, redirect, request, url_for, session, flash, abort
from pymongo import Connection
from bson import ObjectId

import requests

#----------------------------------------------------------------------------------------------
# configuration part
CLIENT_ID = 823
CLIENT_SECRET = 'oudrxrmwjiuiuttffnp6'
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = "https://api.put.io/v2/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s"
AUTH_URL = "https://api.put.io/v2/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s" % (CLIENT_ID, REDIRECT_URI)

#-----------------------------------------------------------------------------------------------
# SoundPut
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ajk85665657765xaswa56da67z5d67'

#------------------------------------DATABASE--------------------------------------------------
# Connect to DB
# Configuration properties used.
connection = Connection('localhost', 27017)
db = connection.soundput

#------------------------------------FUNCTIONS--------------------------------------------------


@app.before_request
def set_user():
    g.user = None
    if 'user_id' in session:
        oid = ObjectId(session['user_id'])
        g.user = db.users.find_one({'_id': oid})


@app.route('/')
def index():
    return render_template('index.html')


# Action when 'LOGIN' button click
# Redirect the user to callback url to login it's put.io account
@app.route('/login')
def login():
    return redirect(AUTH_URL)


@app.route('/callback')
def putio_callback():
    code = request.args.get('code')
    if not code:
        abort(401)

    url = TOKEN_URL % (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, code)
    r = requests.get(url)
    assert r.status_code == 200
    token = json.loads(r.content)['access_token']

    user = db.users.find_one({'token': token})
    if user:
        user_id = user['_id']
    else:
        user_id = db.users.insert({'token': token})

    session['user_id'] = str(user_id)
    return redirect(url_for('index'))


@app.route('/files')
def show_files():
    c = putio.Client(g.user['token'])
    return str(c.File.list())


if __name__ == '__main__':
    app.run(debug=True)
