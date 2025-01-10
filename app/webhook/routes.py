import logging
import os
from flask import Blueprint, request, jsonify
from dateutil import parser
from pytz import timezone, utc
from app.extensions import mongo
from flask import send_from_directory

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Enum for the actions


class ActionEnum:
    PUSH = "PUSH"
    PULL_REQUEST = "PULL_REQUEST"
    MERGE = "MERGE"


webhook_blueprint = Blueprint("webhook", __name__)


@webhook_blueprint.route('/')
def home():
    # Ensure that 'static' is the correct directory for serving your HTML file
    return send_from_directory(os.path.join(os.getcwd(), 'static'), 'index.html')


def parse_timestamp(timestamp):
    """Parse and convert timestamp to ISO format."""
    return parser.parse(timestamp).strftime("%d %B %Y - %I:%M %p UTC")

# Uncomment below function if IST time is required
# def parse_timestamp(timestamp):
#     """Parse and convert UTC timestamp to IST format."""
#     # Parse the UTC timestamp
#     utc_time = parser.parse(timestamp)

#     # Convert to IST
#     ist = timezone('Asia/Kolkata')
#     ist_time = utc_time.astimezone(ist)

#     # Format the IST time
#     return ist_time.strftime("%d %B %Y - %I:%M %p IST")


@webhook_blueprint.route('/webhook/events', methods=['GET'])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)
    result = [
        {
            "event": e["action"],
            "author": e["author"],
            "from_branch": e.get("from_branch", None),
            "to_branch": e.get("to_branch", None),
            "timestamp": e["timestamp"],
        }
        for e in events
    ]
    return jsonify(result)


@webhook_blueprint.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    headers = request.headers
    event = headers.get("X-GitHub-Event")
    data = request.json

    record = {"action": event}

    if event == "push":
        record["action"] = ActionEnum.PUSH
        # Use the commit hash as request_id
        record["request_id"] = data["head_commit"]["id"]
        record["author"] = data["pusher"]["name"]
        # For push, the branch can be extracted from ref
        record["from_branch"] = None
        record["to_branch"] = data["ref"].split(
            "/")[-1]  # Extract the branch name from ref
        record["timestamp"] = parse_timestamp(data["head_commit"]["timestamp"])

    elif event == "pull_request" and data["action"] in ["opened", "closed"]:
        record["action"] = ActionEnum.PULL_REQUEST
        # Using the PR ID for pull requests
        record["request_id"] = data["pull_request"]["id"]
        record["author"] = data["pull_request"]["user"]["login"]
        record["from_branch"] = data["pull_request"]["head"]["ref"]
        record["to_branch"] = data["pull_request"]["base"]["ref"]
        record["timestamp"] = parse_timestamp(
            data["pull_request"]["created_at"])

        if data["action"] == "closed" and data["pull_request"]["merged"]:
            record["action"] = ActionEnum.MERGE
    else:
        return jsonify({"message": "Unsupported event"}), 400

    # Insert record into MongoDB
    mongo.db.events.insert_one(record)

    return jsonify({"message": "Event received", "data": data}), 200
