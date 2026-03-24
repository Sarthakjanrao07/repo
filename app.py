from flask import Flask, request, jsonify
import asyncio
from crawl4ai import AsyncWebCrawler

app = Flask(__name__)

async def crawl_async(url):
    async with AsyncWebCrawler(
        headless=True,
        browser_type="chromium"
    ) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown


@app.route('/crawl', methods=['POST'])
def crawl_api():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL missing"}), 400

        url = data["url"]

        # ✅ FIX (MOST IMPORTANT)
        result = asyncio.run(crawl_async(url))

        return jsonify({
            "success": True,
            "data": result[:2000]  # limit for safety
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Crawl4AI API is running ✅"
