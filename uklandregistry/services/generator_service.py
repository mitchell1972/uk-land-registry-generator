"""
Application data generator service.

This service generates random or specified application data for the UK Land Registry.
"""
import random
import logging
import json
from datetime import datetime, timedelta, date
from ..models.models import Application
from ..repositories.application_type_repository import ApplicationTypeRepository
from ..repositories.application_repository import ApplicationRepository
from ..config import db_manager
from ..utils.sample_data import (
    SAMPLE_ADDRESSES, SAMPLE_NAMES, SAMPLE_COMPANIES, 
    SAMPLE_LENDERS, APPLICATION_STATUSES, CORRECTION_REASONS
)

logger = logging.getLogger(__name__)


class GeneratorService:
    """Service for generating application data"""
    
    def __init__(self, session=None):
        """
        Initialize generator service.
        
        Args:
            session: SQLAlchemy session to use. If None, a new session is created.
        """
        # Create a new session if none is provided
        self.session = session or db_manager.get_session()
        # Share the same session between repositories
        self.app_type_repo = ApplicationTypeRepository(self.session)
        self.app_repo = ApplicationRepository(self.session)
    
    def random_date(self, start_date=None, days_back=365):
        """
        Generate a random date within the specified range.
        
        Args:
            start_date: Starting date for generation. Defaults to today.
            days_back: Number of days to go back (positive) or forward (negative).
            
        Returns:
            A date object
        """
        if start_date is None:
            start_date = datetime.now().date()
        elif isinstance(start_date, datetime):
            start_date = start_date.date()
        
        # Handle future dates (negative days_back) properly
        if days_back < 0:
            # For future dates, days_back is negative, so we need to add days
            random_days = random.randint(1, abs(days_back))
            return start_date + timedelta(days=random_days)
        else:
            # For past dates, subtract random number of days
            random_days = random.randint(0, days_back)
            return start_date - timedelta(days=random_days)
    
    def generate_reference(self):
        """
        Generate a unique reference number for an application.
        
        Returns:
            String reference in format LR123456X
        """
        return f"LR{random.randint(100000, 999999)}{chr(random.randint(65, 90))}"
    
    def generate_random_application(self, app_type_name=None):
        """
        Generate a random application based on an application type.
        
        Args:
            app_type_name: Name of the application type. If None, a random type is used.
            
        Returns:
            Application object and a dictionary with application data
        """
        try:
            # Select application type
            if app_type_name:
                # Get the specific application type from database
                db_app_type = self.app_type_repo.get_by_name(app_type_name)
                if not db_app_type:
                    logger.error(f"Application type '{app_type_name}' not found in database")
                    raise ValueError(f"Application type '{app_type_name}' not found in database")
            else:
                # Random selection
                all_types = self.app_type_repo.get_all()
                if not all_types:
                    logger.error("No application types found in database")
                    raise ValueError("No application types found in database")
                db_app_type = random.choice(all_types)
            
            # Generate a reference number
            reference = self.generate_reference()
            
            # Select random applicants (1-2)
            num_applicants = random.randint(1, 2)
            if random.random() < 0.3:  # 30% chance of company applicant
                applicants = random.sample(SAMPLE_COMPANIES, min(num_applicants, len(SAMPLE_COMPANIES)))
            else:
                applicants = random.sample(SAMPLE_NAMES, min(num_applicants, len(SAMPLE_NAMES)))
            
            # Select a random property
            property_address = random.choice(SAMPLE_ADDRESSES)
            
            # Generate random dates
            submission_date = self.random_date(days_back=180)
            expected_completion = self.random_date(
                start_date=submission_date,
                days_back=-random.randint(10, 90)  # Future date
            )
            
            # Select a random form from the application type
            forms = db_app_type.forms
            selected_form = random.choice(forms) if forms else "N/A"
            
            # Generate status
            statuses, weights = zip(*APPLICATION_STATUSES.items())
            status = random.choices(statuses, weights=weights, k=1)[0]
            
            # Create application instance
            application = Application(
                reference=reference,
                application_type_id=db_app_type.id,  # Use ID instead of object to avoid session issues
                property_address=property_address,
                applicants=applicants,
                submission_date=submission_date,
                expected_completion_date=expected_completion,
                status=status,
                priority=random.randint(1, 5),
                form_used=selected_form
            )
            
            # Add type-specific fields
            if "Charges/Mortgages" in db_app_type.name or "Charge" in db_app_type.name:
                application.lender = random.choice(SAMPLE_LENDERS)
                application.loan_amount = random.randint(50000, 500000)
            
            if "Corrections" in db_app_type.name:
                application.reason_for_correction = random.choice(CORRECTION_REASONS)
            
            # Convert to dictionary for JSON export or printing
            app_dict = {
                "reference": application.reference,
                "application_type": db_app_type.name,
                "description": db_app_type.description,
                "form_used": application.form_used,
                "property_address": application.property_address,
                "applicants": application.applicants,
                "submission_date": application.submission_date.strftime("%Y-%m-%d"),
                "expected_completion_date": application.expected_completion_date.strftime("%Y-%m-%d"),
                "status": application.status,
                "priority": application.priority
            }
            
            if application.lender:
                app_dict["lender"] = application.lender
                app_dict["loan_amount"] = application.loan_amount
            
            if application.reason_for_correction:
                app_dict["reason_for_correction"] = application.reason_for_correction
            
            return application, app_dict
            
        except Exception as e:
            logger.error(f"Error generating random application: {e}")
            raise
    
    def generate_applications(self, type_counts=None, total_count=10):
        """
        Generate applications with specified counts by type or a total count of random applications.
        
        Args:
            type_counts: Dictionary mapping application type names to counts
            total_count: Total number of random applications to generate if type_counts not provided
            
        Returns:
            List of application dictionaries
        """
        app_dicts = []
        applications = []
        
        try:
            if type_counts:
                # Generate specific counts for each type
                for app_type_name, count in type_counts.items():
                    logger.info(f"Generating {count} applications of type '{app_type_name}'")
                    for _ in range(count):
                        application, app_dict = self.generate_random_application(app_type_name)
                        applications.append(application)
                        app_dicts.append(app_dict)
            else:
                # Generate random applications up to total_count
                logger.info(f"Generating {total_count} random applications")
                for _ in range(total_count):
                    application, app_dict = self.generate_random_application()
                    applications.append(application)
                    app_dicts.append(app_dict)
            
            # Add applications to database
            self.app_repo.add_bulk(applications)
            logger.info(f"Added {len(applications)} applications to database")
            
        except Exception as e:
            logger.error(f"Error generating applications: {e}")
            raise
        
        return app_dicts
    
    def save_to_json(self, applications, filename="land_registry_test_data.json"):
        """
        Save applications to a JSON file.
        
        Args:
            applications: List of application dictionaries
            filename: Name of the file to save to
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w') as f:
                json.dump(applications, f, indent=2)
            logger.info(f"Saved {len(applications)} applications to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving applications to JSON: {e}")
            return False
    
    def format_application_for_display(self, app_dict):
        """
        Format an application dictionary for display.
        
        Args:
            app_dict: Application dictionary
            
        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 60)
        output.append(f"Reference: {app_dict['reference']} - {app_dict['application_type']}")
        output.append(f"Status: {app_dict['status']} (Priority: {app_dict['priority']})")
        output.append(f"Property: {app_dict['property_address']}")
        output.append(f"Applicants: {', '.join(app_dict['applicants'])}")
        output.append(f"Submitted: {app_dict['submission_date']} - Expected completion: {app_dict['expected_completion_date']}")
        output.append(f"Form: {app_dict['form_used']}")
        
        # Print conditional fields
        if "lender" in app_dict:
            output.append(f"Lender: {app_dict['lender']} (£{app_dict['loan_amount']})")
        if "reason_for_correction" in app_dict:
            output.append(f"Correction reason: {app_dict['reason_for_correction']}")
        
        output.append("=" * 60)
        return "\n".join(output)
    
    def close(self):
        """Close repository sessions"""
        self.session.close()
        logger.debug("Generator service session closed")
