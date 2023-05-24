def validate_post(raw_json):
    match raw_json:
        case {"text": str(), "author_id": int()}:
            return dict(raw_json)


def validate_user(raw_json):
    match raw_json:
        case {"name": str()}:
            return dict(raw_json)
