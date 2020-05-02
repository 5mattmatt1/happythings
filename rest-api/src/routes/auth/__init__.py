from .login import Login
from .logout import LogoutAccess, LogoutRefresh
from .refresh import Refresh
from .register import Register

def init_auth(api):
    print("Init Auth")
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(LogoutAccess, '/api/auth/logout/access')
    api.add_resource(LogoutRefresh, '/api/auth/logout/refresh')
    api.add_resource(Refresh, '/api/auth/refresh')
    api.add_resource(Register, '/api/auth/register')