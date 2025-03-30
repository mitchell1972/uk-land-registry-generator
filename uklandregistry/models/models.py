"""
Database models for the UK Land Registry application.
"""
from sqlalchemy import Column, Integer, String, Date, JSON, Text, ForeignKey, Float
# Updated import for SQLAlchemy 2.0 compatibility
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ApplicationType(Base):
    """Model for application types"""
    __tablename__ = 'application_types'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50))  # 'core' or 'additional'
    name = Column(String(100), unique=True)
    description = Column(Text)
    forms = Column(JSON)
    
    applications = relationship("Application", back_populates="application_type")
    
    def __repr__(self):
        return f"<ApplicationType(name='{self.name}')>"


class Application(Base):
    """Model for land registry applications"""
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    reference = Column(String(20), unique=True)
    application_type_id = Column(Integer, ForeignKey('application_types.id'))
    property_address = Column(Text)
    applicants = Column(JSON)  # JSON array of applicant names
    submission_date = Column(Date)
    expected_completion_date = Column(Date)
    status = Column(String(30))
    priority = Column(Integer)
    form_used = Column(String(100))
    
    # Optional fields that may not be present for all application types
    lender = Column(String(100), nullable=True)
    loan_amount = Column(Float, nullable=True)
    reason_for_correction = Column(String(100), nullable=True)
    
    application_type = relationship("ApplicationType", back_populates="applications")
    
    def __repr__(self):
        return f"<Application(reference='{self.reference}', type='{self.application_type.name if self.application_type else None}')>"
