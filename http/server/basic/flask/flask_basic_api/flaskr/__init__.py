from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from .storage import Storage

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

stor = Storage(db)

from flaskr.routes import bp

app.register_blueprint(bp)


@app.errorhandler(404)
def handle_not_found(_):
    response = jsonify({"error": "Not Found"})
    response.status_code = 404
    return response
