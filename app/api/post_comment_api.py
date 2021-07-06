from flask_restful import Resource
from flask import jsonify, request, abort
from app.services import post_comment_service
from app.rbac import rbac


class PostComentAPI(Resource):
    method_decorators = {
        "post": [rbac.Allow(["user", "agent"])],
    }

    def get(self, post_id):
        return jsonify(post_comment_service.get_comments(post_id))

    def post(self, post_id):
        comment_dict = request.get_json()
        return jsonify(post_comment_service.create_comment(post_id, comment_dict))