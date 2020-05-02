from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import get_raw_jwt, jwt_refresh_token_required, jwt_required

import models

class LogoutResource(Resource):
    def post(self):
        jti = get_raw_jwt()['jti']
        
        revoked_token = models.RevokedToken(jti=jti)
        
        # NOTE: Could error should handle that
        models.sa.session.add(revoked_token)
        models.sa.session.commit()

        return jsonify({})

class LogoutAccess(LogoutResource):
    @jwt_required
    def post(self):
        return super(LogoutRefresh, self).post()

class LogoutRefresh(LogoutResource):
    @jwt_refresh_token_required
    def post(self):
        return super(LogoutRefresh, self).post()