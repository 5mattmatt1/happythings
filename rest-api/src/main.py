from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask_migrate import init, migrate, upgrade

from models import init_models
from routes import init_routes

SQLALCHEMY_DATABASE_URI = 'postgresql://developer:FasraThuas@123!@localhost:5433/happy_things'

def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)

def main():
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