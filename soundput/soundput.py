# Burak Tekin
# Istanbul Bilgi University
# Department of Computer Science
# Sources:
#     *http://flask.pocoo.org/docs/tutorial/#tutorial)
#     *put.io API
#     *MongoDB
#-----------------------------------------------------------------------------

import json, pymongo, putio
import requests

from flask import Flask, g, render_template, redirect, request, url_for, session, flash, abort
from pymongo import Connection
from bson import ObjectId

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


#Check user session for each request.
@app.before_request
def set_user():
    g.user = None
    if 'user_id' in session:
        oid = ObjectId(session['user_id'])
        g.user = db.users.find_one({'_id': oid})


#Welcome Page.
@app.route('/')
def index():
    return render_template('index.html')


# Action when 'LOGIN' button click.
# Redirect the users to callback url to login their put.io account.
@app.route('/login')
def login():
    return redirect(AUTH_URL)


#Callback action - redirect users to their personal home pages after they login.
@app.route('/callback')
def putio_callback():
    code = request.args.get('code')
    if not code:
        abort(401)#Authorization problem occured!

<<<<<<< HEAD
    #generate url to get/access token.
=======
    #generate url to get||access token.
>>>>>>> f688774064160de3fa8cc3af12c876b82ddead6e
    url = TOKEN_URL % (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, code)

    r = requests.get(url)
    assert r.status_code == 200
<<<<<<< HEAD

    #held token if exists...
    token = json.loads(r.content)['access_token']

    #check user's token exist or not in DB
    user = db.users.find_one({'token': token})

=======
    token = json.loads(r.content)['access_token']#held token if exists...

    user = db.users.find_one({'token': token})#check user's token exist or not in DB
>>>>>>> f688774064160de3fa8cc3af12c876b82ddead6e
    if user:
        user_id = user['_id']
    else:
        user_id = db.users.insert({'token': token})

    session['logged_in'] = True
    session['user_id'] = str(user_id)

    #------- Get files from server ------#

    #Generate a client with token we already had.
    client = putio.Client(token)

    #get user information.
    account_info = client.request("/account/info", method='GET')
    account = account_info['info']


    #check extension is in suitable audio format or not and fetch files.

    dict = client.request("/files/search/ext:mp3", method='GET')
    files = dict['files']
    files = [file for file in files]
<<<<<<< HEAD
    #get number of files.
    length = len(files)

=======
>>>>>>> f688774064160de3fa8cc3af12c876b82ddead6e
    #Insert Files into DB.
    db.user_files.insert(sorted(files))
    return render_template('home.html', files=files, length=length, account=account)


#Logout action
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
