from flaskr import db, ma


class User(db.Model):
    __tablename__ = "tb_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
