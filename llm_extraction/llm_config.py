from typing import Optional, Dict, Any


class LLMExtractionConfig:
    """Basic configuration class for LLM extraction"""
    
    def __init__(
        self,
        provider: str = "openai/gpt-4o-mini",
        api_token: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 8000,
        top_p: float = 0.9
    ):
        """
        Initialize basic LLM configuration
        """
        self.provider = provider
        self.api_token = api_token
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
    
    def get_extra_args(self) -> Dict[str, Any]:
        """Get extra arguments for LLM configuration"""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }
    
    def __str__(self):
        return f"LLMExtractionConfig(provider={self.provider}, max_tokens={self.max_tokens})"


# Simple preset configurations
class LLMConfigPresets:
    """Basic configuration presets"""
    
    @staticmethod
    def openai_fast() -> LLMExtractionConfig:
        """Fast OpenAI configuration"""
        return LLMExtractionConfig(
            provider="openai/gpt-4o-mini",
            temperature=0.1,
            max_tokens=8000
        )
    
    @staticmethod
    def ollama_local() -> LLMExtractionConfig:
        """Local Ollama configuration"""
        return LLMExtractionConfig(
            provider="ollama/llama3.2",
            api_token=None,
            temperature=0.1,
            max_tokens=8000
        )
