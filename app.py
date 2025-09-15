# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import logging
import sys
import traceback

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("chatbot-backend")

app = Flask(__name__)
# Allow cross-origin requests to /chat from any origin (OK for testing; restrict in production)
CORS(app, resources={r"/chat": {"origins": "*"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    user_message = (data or {}).get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # lightweight system prompt; adjust as needed
        messages = [
            {"role": "system", "content": "You are a helpful assistant for Invader FX."},
            {"role": "user", "content": user_message}
        ]

        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = resp["choices"][0]["message"]["content"]
        return jsonify({"reply": reply}), 200

    except Exception as e:
        # Log full exception to Render logs for debugging
        logger.exception("OpenAI request failed")
        # Return a simple error message to the frontend
        return jsonify({"error": "Server error contacting OpenAI", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
