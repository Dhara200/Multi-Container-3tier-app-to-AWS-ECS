from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "waste_db")

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    role = db.Column(db.String(20))


class WasteRequest(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    location = db.Column(db.String(255))
    waste_type = db.Column(db.String(100))
    status = db.Column(db.String(50))


@app.route("/")
def home():
    return jsonify({"message": "Waste API Running"})


@app.route("/request", methods=["POST"])
def create_request():

    data = request.json

    req = WasteRequest(
        user_id=data["user_id"],
        location=data["location"],
        waste_type=data["waste_type"],
        status="Pending"
    )

    db.session.add(req)
    db.session.commit()

    return jsonify({"message": "Request Created"})


@app.route("/requests")
def get_requests():

    requests = WasteRequest.query.all()

    output = []

    for r in requests:
        output.append({
            "id": r.id,
            "location": r.location,
            "waste_type": r.waste_type,
            "status": r.status
        })

    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)