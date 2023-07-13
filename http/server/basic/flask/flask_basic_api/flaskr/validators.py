from typing import Dict, Optional, Set, Tuple, Type, Union

from marshmallow import ValidationError

from .schemas import PostSchema, UserSchema


def check_keys(keys: Set[str], raw_json: Dict) -> Optional[Exception]:
    if set(raw_json.keys()) != keys:
        diff = set(raw_json.keys()) - keys
        return ValidationError("unkrown keys: %s" % ", ".join(diff))


ValidationResult = Tuple[Dict, Optional[Exception]]


def base_validator(
    raw_json: Dict,
    keys: Set[str],
    schema: Union[Type[UserSchema], Type[PostSchema]],
) -> ValidationResult:
    if err := check_keys(keys, raw_json):
        return {}, err
    try:
        r = schema().load(raw_json)
        if not r or not isinstance(r, Dict):
            raise Exception("can't dump user")
        return r, None
    except ValidationError as e:
        return {}, e


def validate_post(raw_json: Dict) -> ValidationResult:
    return base_validator(raw_json, set(["author_id", "text"]), PostSchema)


def validate_user(raw_json: Dict) -> ValidationResult:
    return base_validator(raw_json, set(["name"]), UserSchema)
