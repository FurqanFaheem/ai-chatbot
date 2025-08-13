from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from provider import chat_with_llm

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()

    if not msg:
        return jsonify({"error": "Message is required"}), 400

    try:
        reply = chat_with_llm(msg)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
