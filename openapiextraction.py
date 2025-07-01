import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig,CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
from dotenv import load_dotenv
import sys
from schema import OpenAIModelFee
from typing import Dict,Optional
load_dotenv()


async def extract_structured_data_using_llm(
   provider: str, api_token: str, extra_headers: Optional[Dict[str, str]] = None
):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    if api_token is None and not provider.startswith("ollama"):
        print(f"API token is required for {provider}. Skipping this example.")
        return


    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 2000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config = LLMConfig(provider=provider,api_token=api_token),
            schema=OpenAIModelFee.model_json_schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content.""",
            extra_args=extra_args,
        ),
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
    model = os.environ.get("TARGET_MODEL")
    if model is None:

        raise ValueError("The provided model is not set")
    asyncio.run(
        extract_structured_data_using_llm(
            provider=model, api_token= None
        )
    )

