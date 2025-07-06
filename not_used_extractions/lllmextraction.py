import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig,CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
from dotenv import load_dotenv
import sys
import yaml
from schema import WhoIsHiring
from typing import Dict,Optional
load_dotenv()

async def extract_structured_data_using_llm():

    print("Extracting structured data using LLM")

    # Loading configurations from YAML
    with open("extract_llm.yml", "r") as f:
        config = yaml.safe_load(f)

    #We use ollama to extract the scraped content into an appropriate JSON format
    strategy = LLMExtractionStrategy(
            llm_config = LLMConfig(provider=config["provider"], api_token=config["api_token"]),
            schema=WhoIsHiring.model_json_schema(),
            extraction_type="schema",
            extra_args=config["params"],
            instruction= """From the crawled content, extract all mentioned model names. Do not miss any models in the entire content.""",
        )
    
    #Building the crawler configurations for the LLM extraction
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        url = os.environ.get("TARGET_URL_JOBS_LOCAL")
        if url is None:
            raise ValueError("TARGET_URL environment variable is not set.")
        result = await crawler.arun(
            url=url, config=crawler_config
        )

        if not result.success:
            print(f"Crawl failed: {result.error_message}")
            print(f"Status code: {result.status_code}")

        else:
           print(result.extracted_content)

if __name__ == "__main__":
    model = os.environ.get("TARGET_MODEL")
    if model is None:

        raise ValueError("The provided model is not set")
    asyncio.run(
        extract_structured_data_using_llm()
    )

