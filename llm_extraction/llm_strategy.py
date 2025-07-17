from crawl4ai import LLMExtractionStrategy, LLMConfig
from llm_config import LLMExtractionConfig
from jobs_schema import JobPostings


class BasicLLMExtractor:
    """Basic LLM extraction strategy creator"""
    
    def __init__(self, config: LLMExtractionConfig):
        self.config = config
        self.instruction = """
        Extract job postings from HackerNews hiring content.
        
        For each job posting, find:
        1. Company name (required)
        2. Position/role title (required)  
        3. Location (if mentioned)
        4. Technologies mentioned
        5. Contact information
        
        Be precise and extract only what is clearly mentioned.
        """
    
    def create_strategy(self) -> LLMExtractionStrategy:
        # Create LLM config
        llm_config = LLMConfig(
            provider=self.config.provider,
            api_token=self.config.api_token
        )
        
        # Create and return extraction strategy
        return LLMExtractionStrategy(
            llm_config=llm_config,
            schema=JobPostings.model_json_schema(),
            extraction_type="schema",
            instruction=self.instruction,
            extra_args=self.config.get_extra_args()
        )