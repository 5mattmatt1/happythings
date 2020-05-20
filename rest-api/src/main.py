import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import init, migrate, upgrade

from dotenv import load_dotenv

from models import init_models
from routes import init_routes
from sms import send_request
# Named websocket to avoid collisions
from websocket import socketio, init_socketio

def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)

def main():
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    TWILIO_AC_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'some-secret-key'
    # Fixes problem with flask-restful and flask-jwt-extended
    app.config['PROPAGATE_EXCEPTIONS'] = True

    cors = CORS(app)

    jwt = JWTManager(app)
    jwt.token_in_blacklist_loader(check_if_token_in_blacklist)

    init_models(app)
    api = init_routes(app)
    init_socketio(app)

    socketio.run(app, debug=False)

if __name__ == "__main__":
    main()