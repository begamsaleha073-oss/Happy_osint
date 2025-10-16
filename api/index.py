import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

LEAKOSINT_URL = "https://leakosintapi.com/"
API_TOKEN = os.getenv("API_TOKEN")  # Vercel पर env variable में डालना है
LANG = "en"
LIMIT = 300


@app.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Missing search query"}), 400

        payload = {
            "token": API_TOKEN,
            "request": query,
            "limit": LIMIT,
            "lang": LANG
        }

        # call LeakOSINT API
        r = requests.post(LEAKOSINT_URL, json=payload, timeout=30)
        try:
            result = r.json()
        except Exception:
            return jsonify({"error": "Invalid response from LeakOSINT API"}), 500

        if "Error code" in result:
            return jsonify({"error": result["Error code"]}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
