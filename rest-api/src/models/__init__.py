from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from passlib.hash import pbkdf2_sha256 as sha256

migrate = Migrate()
sa = SQLAlchemy()

class User(sa.Model):
    __tablename__ = "user"
    
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.TEXT, unique=True, nullable=False)
    password = sa.Column(sa.TEXT, nullable=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, pwd_hash):
        return sha256.verify(password, pwd_hash)

class RevokedToken(sa.Model):
    __tablename__ = "revoked_token"

    id = sa.Column(sa.Integer, primary_key=True)
    jti = sa.Column(sa.String(120))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return bool(cls.query.filter_by(jti = jti).first())

def init_models(app):
    sa.init_app(app)
    migrate.init_app(app, sa)