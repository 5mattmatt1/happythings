import requests

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

import models

class Login(Resource):
    def post(self):
        # TODO: Could fail to decode JSON
        # Add error handling
        in_user = request.get_json(force=True)

        # TODO: Fields might be missing, invalid request
        # JSON error or key missing error???
        username = in_user["username"]
        password = in_user["password"]

        user = models.User.find_by_username(username)
        if not user:
            err_resp = jsonify({
                "error" : {
                    # "code" : 
                    "message" : "Wrong username or password."
                }
            })
            err_resp.status_code = requests.codes.BAD_REQUEST
            return err_resp

        if not models.User.verify_hash(password, user.password):
            err_resp = jsonify({
                "error" : {
                    # "code" : 
                    "message" : "Wrong username or password."
                }
            })
            err_resp.status_code = requests.codes.BAD_REQUEST
            return err_resp

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            "login" : {
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }
        })