"""
Repository for application type database operations.
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import ApplicationType
from ..config import db_manager

logger = logging.getLogger(__name__)


class ApplicationTypeRepository:
    """Repository for application type database operations"""
    
    def __init__(self, session=None):
        """
        Initialize repository with session.
        
        Args:
            session: SQLAlchemy session. If None, a new session is created.
        """
        self.session = session or db_manager.get_session()
    
    def create_table(self):
        """Create the application_types table if it doesn't exist"""
        from ..models.models import Base
        Base.metadata.create_all(db_manager.engine, tables=[ApplicationType.__table__])
        logger.info("Application types table created or verified")
    
    def count(self):
        """Count the number of application types in the database"""
        return self.session.query(ApplicationType).count()
    
    def get_all(self):
        """Get all application types"""
        return self.session.query(ApplicationType).all()
    
    def get_by_name(self, name):
        """Get application type by name"""
        return self.session.query(ApplicationType).filter_by(name=name).first()
    
    def get_by_category(self, category):
        """Get application types by category (core or additional)"""
        return self.session.query(ApplicationType).filter_by(category=category).all()
    
    def add(self, application_type):
        """
        Add a new application type to the database.
        
        Args:
            application_type: ApplicationType object to add
            
        Returns:
            The added ApplicationType object
        """
        try:
            self.session.add(application_type)
            self.session.commit()
            logger.debug(f"Added application type: {application_type.name}")
            return application_type
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error adding application type: {e}")
            raise
    
    def add_bulk(self, application_types):
        """
        Add multiple application types to the database.
        
        Args:
            application_types: List of ApplicationType objects
            
        Returns:
            Number of application types added
        """
        try:
            self.session.add_all(application_types)
            self.session.commit()
            logger.debug(f"Added {len(application_types)} application types")
            return len(application_types)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error bulk adding application types: {e}")
            raise
    
    def update(self, application_type):
        """
        Update an application type in the database.
        
        Args:
            application_type: ApplicationType object to update
            
        Returns:
            The updated ApplicationType object
        """
        try:
            self.session.commit()
            logger.debug(f"Updated application type: {application_type.name}")
            return application_type
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating application type: {e}")
            raise
    
    def delete(self, application_type):
        """
        Delete an application type from the database.
        
        Args:
            application_type: ApplicationType object to delete
            
        Returns:
            True if successful
        """
        try:
            self.session.delete(application_type)
            self.session.commit()
            logger.debug(f"Deleted application type: {application_type.name}")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting application type: {e}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.debug("ApplicationTypeRepository session closed") 