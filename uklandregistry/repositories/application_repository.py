"""
Repository for application database operations.
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Application
from ..config import db_manager

logger = logging.getLogger(__name__)


class ApplicationRepository:
    """Repository for application database operations"""
    
    def __init__(self, session=None):
        """
        Initialize repository with session.
        
        Args:
            session: SQLAlchemy session. If None, a new session is created.
        """
        self.session = session or db_manager.get_session()
    
    def create_table(self):
        """Create the applications table if it doesn't exist"""
        from ..models.models import Base
        Base.metadata.create_all(db_manager.engine, tables=[Application.__table__])
        logger.info("Applications table created or verified")
    
    def count(self):
        """Count the number of applications in the database"""
        return self.session.query(Application).count()
    
    def get_all(self, limit=None, offset=None):
        """
        Get all applications with optional pagination.
        
        Args:
            limit: Maximum number of applications to return
            offset: Number of applications to skip
            
        Returns:
            List of Application objects
        """
        query = self.session.query(Application)
        
        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    
    def get_by_reference(self, reference):
        """Get application by reference"""
        return self.session.query(Application).filter_by(reference=reference).first()
    
    def get_by_type(self, application_type_id, limit=None):
        """
        Get applications by application type ID.
        
        Args:
            application_type_id: ID of the application type
            limit: Maximum number of applications to return
            
        Returns:
            List of Application objects
        """
        query = self.session.query(Application).filter_by(application_type_id=application_type_id)
        
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    
    def get_by_status(self, status, limit=None):
        """
        Get applications by status.
        
        Args:
            status: Status to filter by
            limit: Maximum number of applications to return
            
        Returns:
            List of Application objects
        """
        query = self.session.query(Application).filter_by(status=status)
        
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    
    def add(self, application):
        """
        Add a new application to the database.
        
        Args:
            application: Application object to add
            
        Returns:
            The added Application object
        """
        try:
            self.session.add(application)
            self.session.commit()
            logger.debug(f"Added application: {application.reference}")
            return application
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error adding application: {e}")
            raise
    
    def add_bulk(self, applications):
        """
        Add multiple applications to the database.
        
        Args:
            applications: List of Application objects
            
        Returns:
            Number of applications added
        """
        try:
            self.session.add_all(applications)
            self.session.commit()
            logger.debug(f"Added {len(applications)} applications")
            return len(applications)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error bulk adding applications: {e}")
            raise
    
    def update(self, application):
        """
        Update an application in the database.
        
        Args:
            application: Application object to update
            
        Returns:
            The updated Application object
        """
        try:
            self.session.commit()
            logger.debug(f"Updated application: {application.reference}")
            return application
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating application: {e}")
            raise
    
    def delete(self, application):
        """
        Delete an application from the database.
        
        Args:
            application: Application object to delete
            
        Returns:
            True if successful
        """
        try:
            self.session.delete(application)
            self.session.commit()
            logger.debug(f"Deleted application: {application.reference}")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting application: {e}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.debug("ApplicationRepository session closed") 