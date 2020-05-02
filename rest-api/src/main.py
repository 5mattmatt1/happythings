import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import init, migrate, upgrade

from dotenv import load_dotenv

from models import init_models
from routes import init_routes

def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)

def main():
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'some-secret-key'

    cors = CORS(app)

    jwt = JWTManager(app)
    jwt.token_in_blacklist_loader(check_if_token_in_blacklist)

    init_models(app)
    init_routes(app)
    # with app.app_context():
    #     init()
    #     migrate()
    #     upgrade()

    app.run()

if __name__ == "__main__":
    main()