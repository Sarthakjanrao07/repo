from flask import Flask, request, jsonify
import asyncio
from crawl4ai import AsyncWebCrawler

app = Flask(__name__)

async def crawl(url):
    async with AsyncWebCrawler(
        headless=True,
        browser_type="chromium",
        verbose=True
    ) as crawler:
        result = await crawler.arun(
            url=url,
            bypass_cache=True
        )
        return result.markdown


@app.route('/crawl', methods=['POST'])
def crawl_api():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL missing"}), 400

        url = data["url"]

        # ✅ FIX
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(crawl(url))
        loop.close()

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Crawl4AI API is running ✅"
