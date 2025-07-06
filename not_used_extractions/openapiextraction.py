import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig,CacheMode,CrawlResult
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
from dotenv import load_dotenv
import sys
import yaml
from schema import OpenAIModelFee, WhoIsHiring
from typing import Dict,Optional
load_dotenv()


async def extract_structured_data_using_llm(extra_headers: Optional[Dict[str, str]] = None):
    print(f"\n--- Extracting Structured Data with LLM")
    
    # Loading configurations from YAML
    with open("extract_llm.yml", "r") as f:
        config = yaml.safe_load(f)
    
    strategy = LLMExtractionStrategy(
            llm_config = LLMConfig(provider=config["provider"], api_token=config["api_token"]),
            schema=WhoIsHiring.model_json_schema(),
            extraction_type="schema",
            instruction= """From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content.""",
            extra_args=config["params"],
        )

    #Building the crawler configurations for the LLM extraction
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=100,
        page_timeout=80000,
        extraction_strategy=strategy,
    )

    async with AsyncWebCrawler() as crawler:
        url = os.environ.get("TARGET_URL")
        if url is None:
            raise ValueError("TARGET_URL environment variable is not set.")
        result = await crawler.arun(
            url=url, config=crawler_config
        )

        print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(extract_structured_data_using_llm())

