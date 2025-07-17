import asyncio
from crawl4ai import AsyncWebCrawler
from scraper_config import ScraperConfig

class HackerNewsJobScraper:
    
    def __init__(self):
        self.crawler = None
    
    async def scrape_url(self, url: str) -> dict:
        
        try:
            # Create crawler
            self.crawler = AsyncWebCrawler(headless=True)
            
            # Start crawler
            await self.crawler.__aenter__()

            #We fetch the configurations from scraper_config class
            config = ScraperConfig()
            
            try:
                # Scrape the URL
                result = await self.crawler.arun(url=url,config=config.crawler_run_config)
                
                # Check if scraping was successful
                if result.success:
                    return {
                        'success': True,
                        'content': result.markdown,
                        'url': url
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Scraping failed',
                        'url': url
                    }
                    
            finally:
                # Always close crawler
                await self.crawler.__aexit__(None, None, None)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }


async def run_scraper():
    scraper = HackerNewsJobScraper()
    result = await scraper.scrape_url("https://hnhiring.com/march-2025")
    if result['success']:
        print("Fetched the job openings successfully")
    else:
        print("Failed to fetch the job openings")


if __name__ == "__main__":
    asyncio.run(run_scraper())
    