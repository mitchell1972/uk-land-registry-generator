import pytest
from datetime import date
from uklandregistry.models.models import ApplicationType, Application

def test_create_application_type():
    """Test creating an instance of ApplicationType."""
    app_type = ApplicationType(
        category='core',
        name='First Registration',
        description='Registering land or property for the first time.',
        forms=['FR1', 'DL']
    )
    assert app_type.name == 'First Registration'
    assert app_type.category == 'core'
    assert app_type.forms == ['FR1', 'DL']

def test_create_application():
    """Test creating an instance of Application."""
    # First, create a related ApplicationType instance
    app_type = ApplicationType(
        id=1, # Assign an ID for relationship purposes
        category='core',
        name='First Registration',
        description='Registering land or property for the first time.',
        forms=['FR1', 'DL']
    )

    application = Application(
        reference='AB12345',
        application_type_id=1,
        property_address='1 Example Street, London, EX1 1EX',
        applicants=['John Doe', 'Jane Doe'],
        submission_date=date(2024, 1, 15),
        expected_completion_date=date(2024, 3, 15),
        status='Pending',
        priority=2,
        form_used='FR1',
        application_type=app_type # Associate the ApplicationType instance
    )
    assert application.reference == 'AB12345'
    assert application.status == 'Pending'
    assert application.property_address == '1 Example Street, London, EX1 1EX'
    assert application.applicants == ['John Doe', 'Jane Doe']
    assert application.application_type.name == 'First Registration' # Check relationship

def test_create_application_with_optional_fields():
    """Test creating an Application instance with optional fields."""
    app_type = ApplicationType(
        id=2,
        category='additional',
        name='Charge',
        description='Registering a mortgage.',
        forms=['CH1']
    )

    application = Application(
        reference='CD67890',
        application_type_id=2,
        property_address='2 Test Avenue, Manchester, M1 1AM',
        applicants=['Peter Smith'],
        submission_date=date(2024, 2, 1),
        expected_completion_date=date(2024, 4, 1),
        status='Processing',
        priority=1,
        form_used='CH1',
        lender='Big Bank PLC',
        loan_amount=250000.00,
        application_type=app_type
    )
    assert application.reference == 'CD67890'
    assert application.lender == 'Big Bank PLC'
    assert application.loan_amount == 250000.00
    assert application.application_type.name == 'Charge'
