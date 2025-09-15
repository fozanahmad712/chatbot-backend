from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # you can use gpt-4 if enabled
        messages=[{"role": "user", "content": user_message}]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
