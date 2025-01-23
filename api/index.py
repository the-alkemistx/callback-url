from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "your_verify_token"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403
    elif request.method == "POST":
        data = request.json
        print("Webhook Event:", data)
        return "Event Received", 200

# Export app for Vercel
def handler(request, context):
    return app(request, context)
