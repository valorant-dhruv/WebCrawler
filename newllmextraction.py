import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
from dotenv import load_dotenv
import sys
import yaml
from schema import WhoIsHiring, OpenAIModelFee
from typing import Dict, Optional, List
import json

load_dotenv()

def write_valid_jobs_to_json(jobs_data, filename):
    try:
        # If jobs_data is a string, try to parse it as JSON
        if isinstance(jobs_data, str):
            try:
                parsed_data = json.loads(jobs_data)
                if isinstance(parsed_data, list):
                    # Filter jobs where 'error' is False or not present
                    filtered_jobs = [job for job in parsed_data if not job.get('error', False)]
                else:
                    # If it's not a list, just save the parsed data
                    filtered_jobs = [parsed_data]
            except json.JSONDecodeError:
                # If it's not valid JSON, save it as a text response
                filtered_jobs = [{"raw_response": jobs_data}]
        else:
            # If it's already a list, filter it
            filtered_jobs = [job for job in jobs_data if not job.get('error', False)]
        
        # Write filtered jobs to the specified JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(filtered_jobs, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully wrote {len(filtered_jobs)} jobs to {filename}")
        
    except Exception as e:
        print(f"Error writing to JSON: {e}")
        # Fallback: write the raw data as a string
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(jobs_data))

async def extract_structured_data_using_llm(extract:str):
    print("Extracting structured data using LLM")

    try:
        # Loading configurations from YAML
        with open("extract_llm.yml", "r") as f:
            config = yaml.safe_load(f)
        
        print(f"Loaded config: {config}")
        
        # Validate required config fields
        if "provider" not in config:
            raise ValueError("Provider not specified in config")
        
        # Determine which schema to use based on the task
        target_model = os.environ.get("TARGET_MODEL", "").lower()
        
        if "openai" in extract:
            # Use OpenAI model fee schema
            schema = OpenAIModelFee.model_json_schema()
            url = os.environ.get("TARGET_URL")
            instruction = """From the crawled content, extract OpenAI model information including:
            - model_name: The exact name of the OpenAI model
            - input_fee: The cost per input token
            - output_fee: The cost per output token
            Return the data in the exact JSON schema format specified."""
        if "jobs remote" in extract:
            # Use job hiring schema
            schema = WhoIsHiring.model_json_schema()
            url = os.environ.get("TARGET_URL_JOBS")
            instruction = """From the crawled content, extract job posting information including:
            - company_name_and_location: Name of the company that is hiring along with the location
            - job_description: Description of the job role and requirements
            - technology_stack: Technology stack of the desired candidate the company is looking for
            - application_details: How to apply for the job
            Return the data in the exact JSON schema format specified."""
        else:
            schema = WhoIsHiring.model_json_schema()
            url = os.environ.get("TARGET_URL_JOBS_LOCAL")
            instruction = """From the crawled content, extract job posting information including:
            - company_name_and_location: Name of the company that is hiring along with the location
            - job_description: Description of the job role and requirements
            - technology_stack: Technology stack of the desired candidate the company is looking for
            - application_details: How to apply for the job
            Return the data in the exact JSON schema format specified."""
        
        # Create LLM config with proper provider format
        provider = config["provider"]
        api_token = config.get("api_token")


        llm_config =  LLMConfig(provider=provider,api_token=api_token)
        print(f"Using LLM config: provider={llm_config.provider}, model={getattr(llm_config, 'model', 'default')}")
        
        # Create extraction strategy
        strategy = LLMExtractionStrategy(
            llm_config=llm_config,
            schema=schema,
            extraction_type="schema",
            extra_args=config.get("params", {}),
            instruction=instruction,
        )
        
        # Building the crawler configurations for the LLM extraction
        crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=30,
            page_timeout=80000,
            extraction_strategy=strategy
        )

        async with AsyncWebCrawler() as crawler:
            
            if url is None:
                raise ValueError("TARGET_URL_JOBS_LOCAL environment variable is not set.")
            
            print(f"Crawling URL: {url}")
            
            result = await crawler.arun(url=url, config=crawler_config)
            write_valid_jobs_to_json(result.extracted_content,"jobs.json")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Check environment variables
    url = os.environ.get("TARGET_URL_JOBS_LOCAL")
    if url is None:
        print("Error: TARGET_URL_JOBS_LOCAL environment variable is not set")
        sys.exit(1)
    
    print(f"Target URL: {url}")
    
    asyncio.run(extract_structured_data_using_llm("jobs remote"))