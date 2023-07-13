from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Post(db.Model):
    __tablename__ = "tb_posts"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

    def __init__(self, text, author_id) -> None:
        self.text = text
        self.author_id = author_id


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "author_id")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route("/")
def index():
    posts = Post.query.all()
    res = posts_schema.dump(posts)
    return jsonify(res)


def validate_post(raw_json):
    match raw_json:
        case {"text": str(), "author_id": int()}:
            return dict(raw_json)


@app.route("/post", methods=["POST"])
def add_post():
    resp = make_response()
    if new_post := validate_post(request.json):
        db.session.add(Post(**new_post))
        db.session.commit()
        resp.status_code = 204
    else:
        resp.status_code = 400
    return resp
