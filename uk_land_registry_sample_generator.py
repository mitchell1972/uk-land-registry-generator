#!/usr/bin/env python3
"""
UK Land Registry Sample Generator

This script demonstrates how to use the UK Land Registry application types data
to generate random samples for testing purposes and store them in a PostgreSQL database.
"""

import random
import json
import os
import argparse
from datetime import datetime, timedelta
from uk_land_registry_applications import get_application_types

# Database imports
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create SQLAlchemy base
Base = declarative_base()

# Define database models
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


class LandRegistryTestDataGenerator:
    """Generate test data for UK Land Registry applications with PostgreSQL storage"""
    
    def __init__(self, db_uri=None):
        """Initialize the generator with application types and database connection"""
        self.application_types = get_application_types()
        self.all_types = (
            self.application_types["core_application_types"] + 
            self.application_types["additional_application_types"]
        )
        
        # Default database URI if not provided
        if db_uri is None:
            db_uri = os.environ.get(
                'DATABASE_URI', 
                'postgresql://landregistry:landregistry@localhost:5432/land_registry'
            )
        
        # Connect to database
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        
        # Sample data for generating realistic test cases
        self.sample_addresses = [
            "42 Acacia Avenue, London, EC1A 1BB",
            "15 Windsor Road, Manchester, M1 5RD",
            "7 Royal Crescent, Bath, BA1 2LR",
            "29 Castle Street, Edinburgh, EH1 2ND",
            "8 Harbour View, Cardiff, CF10 4PA",
            "63 The Greenway, Birmingham, B4 7QE",
            "12 Victoria Terrace, Bristol, BS8 4NP",
            "5 Market Square, Oxford, OX1 3HA",
            "22 College Lane, Cambridge, CB2 1TN",
            "37 Riverside Walk, Norwich, NR1 1QE"
        ]
        
        self.sample_names = [
            "John Smith", "Sarah Johnson", "Mohammed Khan", 
            "Emily Williams", "David Brown", "Jessica Taylor",
            "Michael Davies", "Emma Wilson", "James Anderson",
            "Olivia Thomas", "Robert Evans", "Sophia Harris"
        ]
        
        self.sample_companies = [
            "Acme Properties Ltd", "Horizon Developments plc",
            "Oakwood Estates Limited", "City Centre Investments Ltd",
            "Heritage Homes Limited", "Waterfront Development Co.",
            "Metropolitan Land Holdings", "Rural Property Trust"
        ]
    
    def create_database_tables(self):
        """Create all database tables if they don't exist"""
        Base.metadata.create_all(self.engine)
        print("Database tables created or verified.")
    
    def populate_application_types(self):
        """Populate the application_types table from the dictionary"""
        session = self.Session()
        
        # Check if we already have data
        if session.query(ApplicationType).count() > 0:
            print("Application types already in database. Skipping...")
            session.close()
            return
        
        # Add core application types
        for app_type in self.application_types["core_application_types"]:
            db_app_type = ApplicationType(
                category="core",
                name=app_type["name"],
                description=app_type["description"],
                forms=app_type["forms"]
            )
            session.add(db_app_type)
        
        # Add additional application types
        for app_type in self.application_types["additional_application_types"]:
            db_app_type = ApplicationType(
                category="additional",
                name=app_type["name"],
                description=app_type["description"],
                forms=app_type["forms"]
            )
            session.add(db_app_type)
        
        session.commit()
        print(f"Added {session.query(ApplicationType).count()} application types to database.")
        session.close()
    
    def random_date(self, start_date=None, days_back=365):
        """Generate a random date within the specified range"""
        if start_date is None:
            start_date = datetime.now()
        
        # Handle future dates (negative days_back) properly
        if days_back < 0:
            # For future dates, days_back is negative, so we need to add days
            random_days = random.randint(1, abs(days_back))
            return (start_date + timedelta(days=random_days)).date()
        else:
            # For past dates, subtract random number of days
            random_days = random.randint(0, days_back)
            return (start_date - timedelta(days=random_days)).date()
    
    def generate_random_application(self, app_type_name=None):
        """
        Generate a random application based on a specific application type or randomly
        
        Args:
            app_type_name (str, optional): Specific application type name to use. Random if None.
        
        Returns:
            dict: Application data dictionary
        """
        session = self.Session()
        
        # Select application type
        if app_type_name:
            # Get the specific application type from database
            db_app_type = session.query(ApplicationType).filter_by(name=app_type_name).first()
            if not db_app_type:
                session.close()
                raise ValueError(f"Application type '{app_type_name}' not found in database")
        else:
            # Random selection
            db_app_type = random.choice(session.query(ApplicationType).all())
        
        # Generate a reference number
        reference = f"LR{random.randint(100000, 999999)}{chr(random.randint(65, 90))}"
        
        # Select random applicants (1-2)
        num_applicants = random.randint(1, 2)
        if random.random() < 0.3:  # 30% chance of company applicant
            applicants = random.sample(self.sample_companies, num_applicants)
        else:
            applicants = random.sample(self.sample_names, num_applicants)
        
        # Select a random property
        property_address = random.choice(self.sample_addresses)
        
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
        status_options = ["Pending", "Processing", "Completed", "Rejected", "Awaiting Further Information"]
        status_weights = [0.3, 0.3, 0.2, 0.1, 0.1]  # More likely to be pending or processing
        status = random.choices(status_options, weights=status_weights, k=1)[0]
        
        # Create application instance
        application = Application(
            reference=reference,
            application_type=db_app_type,
            property_address=property_address,
            applicants=applicants,
            submission_date=submission_date,
            expected_completion_date=expected_completion,
            status=status,
            priority=random.randint(1, 5),
            form_used=selected_form
        )
        
        # Add type-specific fields
        if "Charges/Mortgages" in db_app_type.name:
            application.lender = random.choice([
                "HSBC Bank", "Barclays", "Lloyds Banking Group", 
                "Nationwide Building Society", "NatWest Group"
            ])
            application.loan_amount = random.randint(50000, 500000)
        
        if "Corrections" in db_app_type.name:
            application.reason_for_correction = random.choice([
                "Address error", "Name misspelling", "Incorrect boundary", 
                "Missing easement", "Incorrect tenure type"
            ])
        
        # Convert to dictionary for printing/JSON
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
        
        session.close()
        return application, app_dict
    
    def generate_test_dataset(self, type_counts=None, total_count=10):
        """
        Generate applications with specified counts per type or a total count of random types
        
        Args:
            type_counts (dict, optional): Dictionary of application type names and counts
            total_count (int, optional): Total count of random applications if type_counts not provided
        
        Returns:
            list: Generated applications as dictionaries
        """
        session = self.Session()
        app_dicts = []
        
        try:
            if type_counts:
                # Generate specific counts for each type
                for app_type_name, count in type_counts.items():
                    print(f"Generating {count} applications of type '{app_type_name}'")
                    for _ in range(count):
                        application, app_dict = self.generate_random_application(app_type_name)
                        session.add(application)
                        app_dicts.append(app_dict)
            else:
                # Generate random applications up to total_count
                print(f"Generating {total_count} random applications")
                for _ in range(total_count):
                    application, app_dict = self.generate_random_application()
                    session.add(application)
                    app_dicts.append(app_dict)
            
            session.commit()
            print(f"Added {len(app_dicts)} applications to database")
        except Exception as e:
            session.rollback()
            print(f"Error generating data: {e}")
        finally:
            session.close()
        
        return app_dicts
    
    def save_to_json(self, dataset, filename="land_registry_test_data.json"):
        """Save the generated dataset to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"Dataset saved to {filename}")
    
    def print_sample(self, sample):
        """Print a formatted sample application"""
        print(f"\n{'=' * 60}")
        print(f"Reference: {sample['reference']} - {sample['application_type']}")
        print(f"Status: {sample['status']} (Priority: {sample['priority']})")
        print(f"Property: {sample['property_address']}")
        print(f"Applicants: {', '.join(sample['applicants'])}")
        print(f"Submitted: {sample['submission_date']} - Expected completion: {sample['expected_completion_date']}")
        print(f"Form: {sample['form_used']}")
        
        # Print conditional fields
        if "lender" in sample:
            print(f"Lender: {sample['lender']} (£{sample['loan_amount']})")
        if "reason_for_correction" in sample:
            print(f"Correction reason: {sample['reason_for_correction']}")
        
        print(f"{'=' * 60}\n")


def get_application_type_names():
    """Get all application type names for argument parsing"""
    app_types = get_application_types()
    return [t["name"] for t in app_types["core_application_types"] + app_types["additional_application_types"]]


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate UK Land Registry application data and store in PostgreSQL")
    parser.add_argument('--db-uri', dest='db_uri', help='PostgreSQL connection URI')
    parser.add_argument('--sample-json', dest='sample_json', help='Save sample as JSON to specified file')
    parser.add_argument('--print-samples', dest='print_samples', type=int, default=5, 
                       help='Number of samples to print (default: 5)')
    
    # Allow specifying counts for each application type
    for app_type in get_application_type_names():
        arg_name = app_type.replace('/', '').replace(' ', '-').lower()
        parser.add_argument(f'--{arg_name}', type=int, default=0,
                         help=f'Number of {app_type} applications to generate')
    
    parser.add_argument('--random-count', type=int, default=20,
                       help='Number of random applications to generate if no specific types requested')
    
    args = parser.parse_args()
    
    # Create generator
    generator = LandRegistryTestDataGenerator(db_uri=args.db_uri)
    
    # Create tables and populate application types
    generator.create_database_tables()
    generator.populate_application_types()
    
    # Check if we have specific type counts
    app_type_names = get_application_type_names()
    type_counts = {}
    total_specified = 0
    
    for app_type in app_type_names:
        arg_name = app_type.replace('/', '').replace(' ', '-').lower()
        count = getattr(args, arg_name.replace('-', '_'), 0)
        if count > 0:
            type_counts[app_type] = count
            total_specified += count
    
    # Generate data
    if total_specified > 0:
        samples = generator.generate_test_dataset(type_counts=type_counts)
    else:
        samples = generator.generate_test_dataset(total_count=args.random_count)
    
    # Print samples
    if args.print_samples > 0:
        print_count = min(args.print_samples, len(samples))
        print(f"\n=== SAMPLE UK LAND REGISTRY APPLICATIONS ({print_count}) ===\n")
        for sample in samples[:print_count]:
            generator.print_sample(sample)
    
    # Save to JSON if requested
    if args.sample_json:
        generator.save_to_json(samples, args.sample_json)
