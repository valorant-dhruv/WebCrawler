from crawl4ai import BrowserConfig, CrawlerRunConfig,CacheMode

class ScraperConfig:
    """Configuration class for HackerNews scraping"""
    
    def __init__(self, extraction_strategy= None):
        self.browser_config = BrowserConfig(
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            verbose=False
        )
        
        self.crawler_run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Always fetch fresh content
            word_count_threshold=30,  # Minimum words for valid content
            extraction_strategy = extraction_strategy, #Can we any extraction strategy such as CSS based or LLM based
            page_timeout=80000 
        )
        