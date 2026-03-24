from flask import Flask, request, jsonify
import asyncio
from crawl4ai import AsyncWebCrawler

app = Flask(__name__)

# async crawl function
async def crawl(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

# API route
@app.route('/crawl', methods=['POST'])
def crawl_api():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL missing"}), 400

        url = data["url"]

        result = asyncio.run(crawl(url))

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Crawl4AI API is running ✅"

# 🔥 IMPORTANT FIX
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
