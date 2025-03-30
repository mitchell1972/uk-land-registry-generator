"""
Database service for initializing and managing database operations.
"""
import logging
from ..config import db_manager
from ..models.models import Base
from ..repositories.application_type_repository import ApplicationTypeRepository
from ..repositories.application_repository import ApplicationRepository
from ..data.application_types import get_application_types
from ..models.models import ApplicationType

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for initializing and managing the database"""
    
    def __init__(self):
        """Initialize database service"""
        self.engine = db_manager.engine
        self.app_type_repo = ApplicationTypeRepository()
        self.app_repo = ApplicationRepository()
    
    def initialize_database(self):
        """Initialize the database by creating tables and loading application types"""
        try:
            self._create_tables()
            self._populate_application_types()
            logger.info("Database initialization complete")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return False
        finally:
            self.app_type_repo.close()
    
    def _create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created or verified")
    
    def _populate_application_types(self):
        """Populate application types if not already populated"""
        if self.app_type_repo.count() > 0:
            logger.info("Application types already populated. Skipping...")
            return
        
        app_types_data = get_application_types()
        app_types = []
        
        # Add core application types
        for app_type in app_types_data["core_application_types"]:
            db_app_type = ApplicationType(
                category="core",
                name=app_type["name"],
                description=app_type["description"],
                forms=app_type["forms"]
            )
            app_types.append(db_app_type)
        
        # Add additional application types
        for app_type in app_types_data["additional_application_types"]:
            db_app_type = ApplicationType(
                category="additional",
                name=app_type["name"],
                description=app_type["description"],
                forms=app_type["forms"]
            )
            app_types.append(db_app_type)
        
        # Add all application types to database
        self.app_type_repo.add_bulk(app_types)
        logger.info(f"Added {len(app_types)} application types to database")
    
    def reset_database(self):
        """Drop all tables and recreate them"""
        try:
            Base.metadata.drop_all(self.engine)
            logger.info("All tables dropped")
            self._create_tables()
            self._populate_application_types()
            logger.info("Database reset complete")
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            return False
        finally:
            self.app_type_repo.close() 