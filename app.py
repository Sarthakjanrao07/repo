from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL missing"}), 400

    url = data["url"]

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        return jsonify({
            "success": True,
            "data": text[:5000]  # limit (optional)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Simple Scraper Running ✅"
