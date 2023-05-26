from flask import Blueprint, jsonify, make_response, request

from flaskr import db
from flaskr.models import Post, PostSchema, User, UserSchema
from flaskr.storage import Storage
from flaskr.utils.validators import validate_post, validate_user

bp = Blueprint("api", __name__, url_prefix="/api")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

stor = Storage(db)


@bp.route("/users")
def fetch_users():
    return jsonify(users_schema.dump(User.query.all()))


@bp.route("/user/<int:id>")
def get_user(id: int):
    return user_schema.dump(User.query.get_or_404(id))


@bp.route("/user", methods=["POST"])
def add_user():
    return "", stor.insert(User, validate_user(request.json))


@bp.route("/user/<int:id>", methods=["PUT"])
def update_user(id: int):
    return "", stor.update(User, id, validate_user(request.json))


@bp.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id: int):
    return "", stor.delete(User, id)


@bp.route("/post", methods=["POST"])
def add_post():
    return "", stor.insert(Post, validate_post(request.json))


@bp.route("/post/<int:id>")
def get_post(id: int):
    return post_schema.dump(Post.query.get_or_404(id))
