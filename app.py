import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC0b6e356f93bf5ceb15430e8b5b83ceae'
    TWILIO_SYNC_SERVICE_SID = 'IS36e59eeb544ea2cbcc480db6c98a154a'
    TWILIO_API_KEY = 'SK1796bb05bdde9006bc41fbbbcaea917d'
    TWILIO_API_SECRET = 'OIKeZXVLsGi9vm1djWbvG6NQQdgfcJak'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    t=request.form['text']
    with open('archita.txt','w') as f:
        f.write(t)
    x="archita.txt"  
    return send_file(x, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
