import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import os
from dotenv import load_dotenv
import sys
load_dotenv()

async def main():
    try:
        browser_conf = BrowserConfig(headless=True) 

        #This will fetch new content each time. By default the cache is enabled
        run_conf = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS
        )

        async with AsyncWebCrawler(config=browser_conf) as crawler:
            url = os.environ.get("TARGET_URL")
            if url is None:
                raise ValueError("TARGET_URL environment variable is not set.")
            result = await crawler.arun(
                url=url,
                config=run_conf
            )
            print(result.markdown)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Unhandled error: {e}", file=sys.stderr)
