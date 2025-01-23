from flask import Flask, request, jsonify

app = Flask(__name__)

# Your custom verification token
VERIFY_TOKEN = "explicit"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    try:
        if request.method == "GET":
            # Verification request from Meta
            verify_token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            
            if verify_token == VERIFY_TOKEN:
                # Return the challenge to verify the URL
                return challenge, 200
            else:
                return "Verification token mismatch", 403
        
        elif request.method == "POST":
            # Handling incoming Webhook events
            data = request.json
            if not data:
                return jsonify({"error": "No JSON payload received"}), 400
            
            # Log the event for debugging
            print("Webhook event received:", data)
            
            # Acknowledge the event
            return jsonify({"status": "Event received"}), 200
    
    except Exception as e:
        # Log the error for debugging
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


# Run the Flask app (for local testing)
if __name__ == "__main__":
    app.run(port=5000)
