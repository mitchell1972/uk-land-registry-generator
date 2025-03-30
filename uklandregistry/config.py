"""
Configuration module for UK Land Registry application.

This module handles configuration loading from environment variables and/or config files.
"""
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    def __init__(self):
        # Database settings
        self.db_user = os.environ.get('DB_USER', 'landregistry')
        self.db_password = os.environ.get('DB_PASSWORD', 'landregistry')
        self.db_host = os.environ.get('DB_HOST', 'localhost')
        self.db_port = os.environ.get('DB_PORT', '5433')
        self.db_name = os.environ.get('DB_NAME', 'land_registry')
        
        # Set up logging
        self.setup_logging()
    
    @property
    def database_uri(self):
        """Get the database URI from configuration"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def setup_logging(self):
        """Configure logging for the application"""
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = logging.INFO
        
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self, config=None):
        self.config = config or Config()
        self.engine = None
        self.Session = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize database engine and session factory"""
        self.engine = create_engine(self.config.database_uri)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()


# Create a default instance of the configuration
config = Config()
db_manager = DatabaseManager(config) 