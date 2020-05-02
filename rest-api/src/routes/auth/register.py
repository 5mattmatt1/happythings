from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

import models

class Register(Resource):
    def post(self):
        # TODO: Could fail to decode JSON
        # Add error handling
        in_user = request.get_json(force=True)

        # TODO: Fields might be missing, invalid request
        # JSON error or key missing error???
        username = in_user["username"]
        password = models.User.generate_hash(in_user["password"])

        if models.User.find_by_username(username):
            err_resp = jsonify({
                "error" : {
                    # "code" : 
                    "message" : "User already exists."
                }
            })
            err_resp.status_code = requests.codes.BAD_REQUEST
            return err_resp

        new_user = models.User(
            username=username,
            password=password
        )

        # Need to handle DB errors...
        models.sa.session.add(new_user)
        models.sa.session.commit()

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            "register" : {
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }
        })