from flask import Blueprint, jsonify, request, render_template
from datetime import datetime
from app.extensions import events_collection, db
import os




webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    try:
        data = request.json

        # event type from headers
        event_type = request.headers.get("X-GitHub-Event")

        if event_type == "push":
            author = data["pusher"]["name"]
            to_branch = data["ref"].split("/")[-1]
            timestamp = data["head_commit"]["timestamp"]
            request_id = data["after"]

            doc = {
                "request_id": request_id,
                "author": author,
                "action": "PUSH",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            events_collection.insert_one(doc)

        elif event_type == "pull_request":

            pr = data["pull_request"]

            author = pr["user"]["login"]
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            timestamp = pr["created_at"]
            request_id = str(pr["id"])

            action_type = "PULL_REQUEST"

            # MERGED PULL Request
            if data["action"] == "closed" and pr["merged"]:
                action_type = "MERGE"
                timestamp = pr["merged_at"]

            doc = {
                "request_id": request_id,
                "author": author,
                "action": action_type,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            events_collection.insert_one(doc)
    except Exception as ex:
        print("error while processing the events", str(ex))

    return jsonify({"status": "success"}), 200



