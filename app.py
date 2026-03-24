from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL missing"}), 400

        url = data["url"]

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()

        return jsonify({
            "success": True,
            "data": text[:2000]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Working ✅"
