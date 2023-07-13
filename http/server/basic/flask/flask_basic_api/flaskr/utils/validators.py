from typing import Optional
from flaskr.models import UserSchema
from flaskr.routes import User


def validate_post(raw_json):
    match raw_json:
        case {"text": str(), "author_id": int()}:
            return dict(raw_json)


def validate_user(raw_json):
    match raw_json:
        case {"name": str()}:
            try:
                return UserSchema().load(raw_json)
            except Exception as e:
                print(repr(e))
