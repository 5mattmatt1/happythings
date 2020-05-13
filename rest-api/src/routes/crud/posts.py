from flask import request, jsonify

from webargs import fields
from webargs.flaskparser import use_kwargs

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime
import requests
import models

class BasePostResource:
    @staticmethod
    def fmt_post(post):
        return {
            "id" : post.id,
            "text" : post.text,
            "poster_id" : post.poster_id,
            "recipient_id" : post.recipient_id,
            "datetime" : post.datetime.isoformat()
        }

class Posts(Resource, BasePostResource):
    @jwt_required
    def get(self):
        posts = models.Post.all()
        return jsonify(list(map(
            self.fmt_post,
            posts
        )))


class Post(Resource, BasePostResource):
    get_args = {"id": fields.Int(required=True)}
    delete_args = {"id": fields.Int(required=True)}

    @jwt_required
    def post(self):
        # TODO: Look into alternatives of jwt_required for expired sessions.
        # jwt.exceptions.ExpiredSignatureError
        in_post = request.get_json(force=True)

        if "user_id" not in in_post:
            username = get_jwt_identity()
            user = models.User.find_by_username(username)
            user_id = user.id
        else:
            user_id = in_post["user_id"]
            user = models.User.find_by_id(user_id)

        if "recipient_id" not in in_post:
            if not user.partner_id:
                err_resp = jsonify({
                    "error" : {
                        "message" : "'recipient' field is required or supplied user must have a NOT NULL 'partner_id'"
                    }
                })
                err_resp.status_code = requests.codes.BAD_REQUEST
                return err_resp
            recipient_id = user.partner_id
        else:
            recipient_id = in_post["recipent_id"]

        if "datetime" not in in_post:
            # TODO: Make this UTC
            in_datetime = datetime.datetime.now()
        else:
            in_datetime = in_post["datetime"]

        if "text" not in in_post:
            err_resp = jsonify({
                "error" : {
                    "message" : "'text' field is required."
                }
            })
            err_resp.status_code = requests.codes.BAD_REQUEST
            return err_resp
        else:
            text = in_post["text"]

        db_post = models.Post(text=text, poster_id=user_id, recipient_id=recipient_id, 
                            datetime=in_datetime)
        models.sa.session.add(db_post)
        models.sa.session.commit()

        return jsonify({})

    @jwt_required
    @use_kwargs(get_args, location="query")
    def get(self, id):
        db_post = models.Post.find_by_id(id)
        if db_post is None:
            err_resp = jsonify({
                "error" : {
                    "message" : "No Post with ID: {}".format(id)
                }
            })
            err_resp.status_code = requests.codes.NOT_FOUND
            return err_resp

        return jsonify(self.fmt_post(db_post))

    @jwt_required
    @use_kwargs(delete_args, location="query")
    def delete(self, id):
        db_post = models.Post.find_by_id(id)
        if db_post is None:
            err_resp = jsonify({
                "error" : {
                    "message" : "No Post with ID: {}".format(id)
                }
            })
            err_resp.status_code = requests.codes.NOT_FOUND
            return err_resp

        models.sa.session.delete(db_post)
        models.sa.session.commit()

        return jsonify({})