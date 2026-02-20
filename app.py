from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///timer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)

# создаём таблицу при старте (важно для gunicorn)
@app.before_request
def create_tables():
    db.create_all()
    if not Timer.query.first():
        db.session.add(Timer(start_time=None))
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    timer = Timer.query.first()
    timer.start_time = datetime.utcnow()
    db.session.commit()
    return jsonify({"status": "started"})

@app.route("/get_time")
def get_time():
    timer = Timer.query.first()
    if timer and timer.start_time:
        diff = datetime.utcnow() - timer.start_time
        return jsonify({"seconds": diff.total_seconds()})
    return jsonify({"seconds": 0})
