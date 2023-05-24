from flask import Blueprint, jsonify, make_response, request

from flaskr import db
from flaskr.models import Post, PostSchema, User, UserSchema
from flaskr.utils.validators import validate_post, validate_user

bp = Blueprint("api", __name__, url_prefix="/api")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("/")
def index():
    posts = Post.query.all()
    res = posts_schema.dump(posts)
    return jsonify(res)


@bp.route("/user", methods=["POST"])
def add_user():
    resp = make_response()
    if new_user := validate_user(request.json):
        db.session.add(User(**new_user))
        db.session.commit()
        resp.status_code = 204
    else:
        resp.status_code = 400
    return resp


@bp.route("/user/<int:id>")
def get_user(id: int):
    return user_schema.dump(User.query.get_or_404(id))


@bp.route("/post", methods=["POST"])
def add_post():
    resp = make_response()
    if new_post := validate_post(request.json):
        db.session.add(Post(**new_post))
        db.session.commit()
        resp.status_code = 204
    else:
        resp.status_code = 400
    return resp


@bp.route("/post/<int:id>")
def get_post(id: int):
    return post_schema.dump(Post.query.get_or_404(id))
