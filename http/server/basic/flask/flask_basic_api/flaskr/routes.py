from typing import Dict
from flask import Blueprint, jsonify, request

from flaskr import stor
from .models import User, Post
from .schemas import UserSchema, PostSchema
from .validators import validate_post, validate_user

bp = Blueprint("api", __name__, url_prefix="/api")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.errorhandler(Exception)
def handle_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = getattr(error, "code", 500)
    return response


@bp.route("/users")
def fetch_users():
    return jsonify(users_schema.dump(User.query.all()))


@bp.route("/users/<int:id>")
def get_user(id: int):
    return user_schema.dump(User.query.get_or_404(id))


@bp.route("/users", methods=["POST"])
def add_user():
    if not isinstance(request.json, Dict):
        return "", 415
    user, err = validate_user(request.json)
    if err:
        return {"error": str(err)}, 400
    return "", stor.insert(User, user)


@bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id: int):
    if not isinstance(request.json, Dict):
        return "", 415
    user, err = validate_user(request.json)
    if err:
        return {"error": str(err)}, 400
    return "", stor.update(User, id, user)


@bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id: int):
    return "", stor.delete(User, id)


@bp.route("/posts")
def fetch_posts():
    return jsonify(posts_schema.dump(Post.query.all()))


@bp.route("/posts/<int:id>")
def get_post(id: int):
    return post_schema.dump(Post.query.get_or_404(id))


@bp.route("/posts", methods=["POST"])
def add_post():
    if not isinstance(request.json, Dict):
        return "", 415
    post, err = validate_post(request.json)
    if err:
        return {"errror": str(err)}, 400
    return "", stor.insert(Post, post)


@bp.route("/posts/<int:id>", methods=["PUT"])
def update_post(id: int):
    if not isinstance(request.json, Dict):
        return "", 415
    post, err = validate_post(request.json)
    if err:
        return {"error": str(err)}, 400
    return "", stor.update(Post, id, post)


@bp.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id: int):
    return "", stor.delete(Post, id)
