import flask
import requests_oauthlib
import os
from flask_sslify import SSLify
import requests


CLIENT_ID = 'example-yxztnmpafj'
CLIENT_SECRET = 'cxmtrmoprqvrqotsydhuhquckbwakesiyvweucpk'

AUTHORIZATION_BASE_URL = "https://app.simplelogin.io/oauth2/authorize"
TOKEN_URL = "https://app.simplelogin.io/oauth2/token"
USERINFO_URL = "https://app.simplelogin.io/oauth2/userinfo"

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)
context = (r'server.crt', r'server.key')
sslify = SSLify(app)


@app.route("/")
def index():
    return """
    <a href="/login">Login with SimpleLogin</a>
    """


@app.route("/login")
def login():
    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri="https://localhost:5000/callback"
    )
    authorization_url, _ = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)

    return flask.redirect(authorization_url)


@app.route("/callback")
def callback():
    print(CLIENT_ID)
    simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID)
    simplelogin.fetch_token(
        TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=flask.request.url
    )

    user_info = simplelogin.get(USERINFO_URL).json()
    return f"""
    User information: <br>
    Name: {user_info["name"]} <br>
    Email: {user_info["email"]} <br>    
    Avatar <img src="{user_info.get('avatar_url')}"> <br>
    <a href="/">Home</a>
    """


if __name__ == "__main__":
    import ssl
    from werkzeug import serving

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(r"C:\Users\kmv7kor\Desktop\ca.crt")
    context.load_cert_chain("server.crt", "server.key")
    serving.run_simple("0.0.0.0", 8000, app, ssl_context=context)
    context = (r'C:\NEFIT\sso\server.crt', r'C:\NEFIT\sso\server.key')
    # app.run(debug=True, ssl_context=context)