# src/scraper/logger.py - Step 4: Simple Logger

import logging
import sys

class ScraperLogger:
    """Simple logger for the scraper"""
    
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup basic logging configuration"""
        # Only setup if no handlers exist (prevents duplicate logs)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            
            # Create simple formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)