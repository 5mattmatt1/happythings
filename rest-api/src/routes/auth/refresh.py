from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_refresh_token_required

class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify({
            "refresh" : {
                "access_token" : access_token
            }
        })