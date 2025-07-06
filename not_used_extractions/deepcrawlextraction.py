import asyncio
from pdb import run
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, ContentRelevanceFilter
import os
from dotenv import load_dotenv
import sys
load_dotenv()

def process_result(result):
    print(f"Content that is being streamed: {result.markdown}")


async def main():

    try:
        browser_conf = BrowserConfig(headless=True) 

        relevance_filter = ContentRelevanceFilter(
            query="San Fransisco",
            threshold=0.7  # Minimum similarity score (0.0 to 1.0)
        )

        strategy = BFSDeepCrawlStrategy(
            max_depth=2,               # Crawl initial page + 2 levels deep
            include_external=False,    # Stay within the same domain
            max_pages=50,              # Maximum number of pages to crawl (optional)
            score_threshold=0.3,       # Minimum score for URLs to be crawled (optional)
            filter_chain=FilterChain([relevance_filter])
        )

        #This will fetch new content each time. By default the cache is enabled
        run_conf = CrawlerRunConfig(
            #Cach control
            cache_mode=CacheMode.ENABLED,

            # Content filtering
            word_count_threshold=100,
            excluded_tags=['form', 'header'],

            # Content processing
            process_iframes=True,
            remove_overlay_elements=True,

            #For scanning complete page
            scan_full_page=True,

            #Deep crawling strategy
            deep_crawl_strategy=strategy,
            stream=True
        )

        async with AsyncWebCrawler(config=browser_conf) as crawler:
            url = os.environ.get("TARGET_URL_JOBS")
            if url is None:
                raise ValueError("TARGET_URL environment variable is not set.")

            async for result in await crawler.arun(url, config=run_conf):
                # Process each result as it becomes available
                process_result(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Unhandled error: {e}", file=sys.stderr)
