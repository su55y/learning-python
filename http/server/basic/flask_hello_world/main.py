from markupsafe import escape
from flask import Flask, request, make_response

app = Flask(__name__)
posts = {}


def add_post(user: str, post: str):
    posts[user].append(post) if user in posts.keys() else posts.setdefault(user, [post])


def get_post(user: str, post_id: int):
    if user_posts := posts.get(user):
        if len(user_posts) > post_id:
            return user_posts[post_id]


def del_post(user: str, post_id: int):
    if user_posts := posts.get(user):
        if len(user_posts) > post_id:
            del user_posts[post_id]
            posts[user] = user_posts
            return True


@app.route("/", methods=["GET"])
def index():
    return posts


@app.route("/<user>", methods=["GET"])
def user_posts(user: str):
    return posts.get(user, {})


@app.route("/<user>/new", methods=["POST"])
def new_post(user: str):
    resp = make_response()
    match data := request.get_json():
        case {"post": str()}:
            if not len(data["post"]):
                resp.set_data(b'{"err": "empty post"}')
            else:
                add_post(user, escape(data["post"]))
                resp.status = 204
        case _:
            resp.status = 400
    return resp


@app.route("/<user>/<int:post_id>", methods=["GET", "DELETE"])
def manage_post(user: str, post_id: int):
    resp = make_response()
    match request.method:
        case "GET":
            if post := get_post(user, post_id):
                resp.set_data(f"{post}".encode())
            else:
                resp.status = 404
        case "DELETE":
            resp.status = 204 if del_post(user, post_id) else 404
        case _:
            resp.status = 405
    return resp
