"""
Configuration module for ArtifactsMmo wrapper
Loads settings from .env file for secure token and character management
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class that loads settings from environment variables"""
    
    def __init__(self):
        self.token = os.getenv('ARTIFACTS_TOKEN')
        self.character_name = os.getenv('CHARACTER_NAME')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # Validate required settings
        if not self.token:
            raise ValueError("ARTIFACTS_TOKEN not found in environment variables. Please check your .env file.")
        
        if not self.character_name:
            raise ValueError("CHARACTER_NAME not found in environment variables. Please check your .env file.")
    
    def __repr__(self):
        return f"Config(character_name='{self.character_name}', log_level='{self.log_level}', token={'*' * 10 + '...' if self.token else 'None'})"

# Create global config instance
config = Config()

# For easy importing
__all__ = ['config'] 