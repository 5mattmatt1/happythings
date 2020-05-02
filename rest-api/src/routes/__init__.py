from flask_restful import Api

api = Api()

def init_routes(app):
    api.init_app(app)
