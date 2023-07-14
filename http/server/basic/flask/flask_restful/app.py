from flask import Flask, request
from flask_marshmallow import Marshmallow, Schema
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
api = Api(app)
db = SQLAlchemy()
ma = Marshmallow(app)
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class UserSchema(Schema):
    class Meta:
        fields = ("id", "name")


with app.app_context():
    db.create_all()

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    def get(self, user_id):
        user = db.get_or_404(User, user_id)
        return user_schema.dump(user)


class UsersResource(Resource):
    def get(self):
        users = db.session.execute(db.select(User).order_by(User.name)).scalars()
        return users_schema.dump(users)

    def post(self):
        data = request.get_json()
        if set(list(data.keys())) != set(["name"]):
            return {"error": "invalid user data"}, 400
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return "", 204


api.add_resource(UserResource, "/users/<user_id>")
api.add_resource(UsersResource, "/users")

if __name__ == "__main__":
    app.run(debug=True)
