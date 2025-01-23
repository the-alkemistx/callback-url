import os
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment variables (replace with your values or use dotenv for loading)
APP_SECRET = os.getenv("APP_SECRET", "bf94edb3ccd35b3d5aa6bf1f8eb26fa3")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "explicit")

# Store received updates for debugging
received_updates = []

def validate_signature(request):
    """Validate X-Hub-Signature header against the request body."""
    signature = request.headers.get("X-Hub-Signature")
    if not signature:
        return False

    method, hash_value = signature.split("=")
    if method != "sha1":
        return False

    expected_hash = hmac.new(
        APP_SECRET.encode("utf-8"),
        request.data,
        hashlib.sha1
    ).hexdigest()

    return hmac.compare_digest(hash_value, expected_hash)

@app.route("/", methods=["GET"])
def home():
    """Display received updates for debugging."""
    return jsonify(received_updates), 200

@app.route("/facebook", methods=["GET", "POST"])
@app.route("/instagram", methods=["GET", "POST"])
@app.route("/threads", methods=["GET", "POST"])
def webhook():
    """Handle verification and incoming webhook events."""
    try:
        if request.method == "GET":
            # Verification request
            mode = request.args.get("hub.mode")
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")

            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Verification token mismatch", 403

        elif request.method == "POST":
            # Validate X-Hub-Signature
            if not validate_signature(request):
                return "X-Hub-Signature not valid", 401

            # Process webhook events
            data = request.json
            if not data:
                return "No JSON payload received", 400

            # Log received update
            print(f"Received update: {data}")
            received_updates.insert(0, data)  # Add to the start of the list
            return jsonify({"status": "Event received"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(port=5000)
