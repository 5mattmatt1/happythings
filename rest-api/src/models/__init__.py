from flask_sqlalchemy import SQLAlchemy

sa = SQLAlchemy()

def init_models(app):
    sa.init_app(app)