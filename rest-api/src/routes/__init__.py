from flask_restful import Api

from .auth import init_auth
from .crud import init_crud

# from webargs import 

def init_routes(app):
    # NOTE: init_app doesn't work the same on Api as it does on SQLAlchemy
    # need to look into that.
    api = Api(app)
    init_auth(api)
    init_crud(api)