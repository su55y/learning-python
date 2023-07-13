from marshmallow import Schema


class UserSchema(Schema):
    class Meta:
        fields = ("id", "name")


class PostSchema(Schema):
    class Meta:
        fields = ("id", "text", "author_id")
