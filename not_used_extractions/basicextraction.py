import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import os
from dotenv import load_dotenv
import sys
load_dotenv()

#This web crawler fetches the data and returns the simple markdown content
async def main():
    try:
        browser_conf = BrowserConfig(headless=True) 

        #This will fetch new content each time. By default the cache is enabled
        run_conf = CrawlerRunConfig(
            #Cach control
            cache_mode=CacheMode.BYPASS,

            # Content filtering
            word_count_threshold=100,
            excluded_tags=['form', 'header'],

            # Content processing
            process_iframes=True,
            remove_overlay_elements=True,

            #For scanning complete page
            scan_full_page=True,
        )

        async with AsyncWebCrawler(config=browser_conf) as crawler:
            url = os.environ.get("TARGET_URL_JOBS_LOCAL")
            if url is None:
                raise ValueError("TARGET_URL environment variable is not set.")
            result = await crawler.arun(
                url=url,
                config=run_conf
            )
            
            if not result.success:
                print(f"Crawl failed: {result.error_message}")
                print(f"Status code: {result.status_code}")
            else:
                print(result.markdown)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Unhandled error: {e}", file=sys.stderr)
