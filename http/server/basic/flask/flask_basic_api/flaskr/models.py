from flaskr import db


class User(db.Model):
    __tablename__ = "tb_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Post(db.Model):
    __tablename__ = "tb_posts"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

    def __init__(self, text, author_id) -> None:
        self.text = text
        self.author_id = author_id
