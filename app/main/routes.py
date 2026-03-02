from flask import Blueprint, render_template, jsonify
from app.extensions import events_collection


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/events")
def get_events():
    events = list(events_collection.find().sort("timestamp", -1))
    
    for event in events:
        event["_id"] = str(event["_id"])
    
    return jsonify(events)