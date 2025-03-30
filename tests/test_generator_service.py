import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime, timedelta
from uklandregistry.services.generator_service import GeneratorService
from uklandregistry.models.models import ApplicationType, Application

# Sample data for mocking repository responses
SAMPLE_APP_TYPE_CORE = ApplicationType(
    id=1,
    category='core',
    name='First Registration',
    description='Registering land or property for the first time.',
    forms=['FR1', 'DL']
)
SAMPLE_APP_TYPE_ADDITIONAL = ApplicationType(
    id=2,
    category='additional',
    name='Charge',
    description='Registering a mortgage.',
    forms=['CH1']
)
ALL_APP_TYPES = [SAMPLE_APP_TYPE_CORE, SAMPLE_APP_TYPE_ADDITIONAL]

@pytest.fixture
def mock_session():
    """Fixture for a mocked SQLAlchemy session."""
    return MagicMock()

@pytest.fixture
def mock_app_type_repo(mocker):
    """Fixture for a mocked ApplicationTypeRepository."""
    repo = MagicMock()
    repo.get_by_name.return_value = SAMPLE_APP_TYPE_CORE # Default mock
    repo.get_all.return_value = ALL_APP_TYPES
    return repo

@pytest.fixture
def mock_app_repo(mocker):
    """Fixture for a mocked ApplicationRepository."""
    repo = MagicMock()
    return repo

@pytest.fixture
def generator_service(mocker, mock_session, mock_app_type_repo, mock_app_repo):
    """Fixture for GeneratorService with mocked dependencies."""
    # Mock the repository instantiation within GeneratorService.__init__
    mocker.patch('uklandregistry.services.generator_service.ApplicationTypeRepository', return_value=mock_app_type_repo)
    mocker.patch('uklandregistry.services.generator_service.ApplicationRepository', return_value=mock_app_repo)
    # Mock db_manager.get_session if GeneratorService creates its own session
    mocker.patch('uklandregistry.services.generator_service.db_manager.get_session', return_value=mock_session)

    # Instantiate the service (repositories will be mocked)
    service = GeneratorService(session=mock_session) # Pass mock session explicitly
    return service

# --- Test Cases ---

def test_random_date_past(generator_service, mocker):
    """Test generating a random date in the past."""
    mock_now = datetime(2024, 3, 30)
    mocker.patch('uklandregistry.services.generator_service.datetime', MagicMock(now=lambda: mock_now))
    mocker.patch('uklandregistry.services.generator_service.random.randint', return_value=10) # Mock random days

    generated_date = generator_service.random_date(days_back=180)
    expected_date = date(2024, 3, 20) # 2024-03-30 - 10 days
    assert generated_date == expected_date

def test_random_date_future(generator_service, mocker):
    """Test generating a random date in the future."""
    start_date = date(2024, 3, 30)
    mocker.patch('uklandregistry.services.generator_service.random.randint', return_value=15) # Mock random days

    generated_date = generator_service.random_date(start_date=start_date, days_back=-30) # days_back is negative
    expected_date = date(2024, 4, 14) # 2024-03-30 + 15 days
    assert generated_date == expected_date

def test_generate_reference(generator_service, mocker):
    """Test the format of the generated reference number."""
    mocker.patch('uklandregistry.services.generator_service.random.randint', side_effect=[123456, ord('X')])
    reference = generator_service.generate_reference()
    assert reference == "LR123456X"

# Removed @patch decorator, using mocker fixture instead
def test_generate_random_application_specific_type(generator_service, mock_app_type_repo, mocker):
    """Test generating an application for a specific type."""
    # Configure mocks for random choices within the method using mocker
    mocker.patch('uklandregistry.services.generator_service.random.randint', side_effect=[1, 2, 30, 3, 2]) # num_applicants, priority, days_back, additional random value, explicit priority
    mocker.patch('uklandregistry.services.generator_service.random.random', return_value=0.5) # Not a company
    mocker.patch('uklandregistry.services.generator_service.random.sample', return_value=['Alice Smith']) # applicants
    mocker.patch('uklandregistry.services.generator_service.random.choice', side_effect=[
        '1 Test Street, Testville, T1 1TT', # address
        'FR1' # form
    ])
    mocker.patch('uklandregistry.services.generator_service.random.choices', return_value=['Pending']) # status

    # Mock date generation
    fixed_date = date(2024, 1, 1)
    generator_service.random_date = MagicMock(return_value=fixed_date)

    app_type_name = 'First Registration'
    application, app_dict = generator_service.generate_random_application(app_type_name)

    mock_app_type_repo.get_by_name.assert_called_once_with(app_type_name)
    assert application.application_type_id == SAMPLE_APP_TYPE_CORE.id
    assert application.applicants == ['Alice Smith']
    assert application.property_address == '1 Test Street, Testville, T1 1TT'
    assert application.form_used == 'FR1'
    assert application.status == 'Pending'
    assert application.priority == 2
    assert app_dict['application_type'] == app_type_name
    # Ensure lender/loan amount are not set for this type
    assert 'lender' not in app_dict
    assert 'loan_amount' not in app_dict

# Removed @patch decorator, using mocker fixture instead
def test_generate_random_application_random_type(generator_service, mock_app_type_repo, mocker):
    """Test generating an application for a random type (Charge)."""
    # Configure mocks using mocker
    # Calls expected: num_applicants, priority, days_back, loan amount for constructor, priority in constructor, another loan_amount for when Charge is detected
    mocker.patch('uklandregistry.services.generator_service.random.randint', side_effect=[2, 3, 30, 150000, 3, 150000])
    mocker.patch('uklandregistry.services.generator_service.random.random', return_value=0.1) # Company applicant
    mocker.patch('uklandregistry.services.generator_service.random.sample', return_value=['Test Corp Ltd', 'Another Ltd']) # applicants
    mocker.patch('uklandregistry.services.generator_service.random.choice', side_effect=[
        SAMPLE_APP_TYPE_ADDITIONAL, # Randomly chosen app type (Charge)
        '2 Corp Avenue, Industrious, I1 1II', # address
        'CH1', # form
        'Mock Lender Inc.' # lender (called because type is Charge)
    ])
    mocker.patch('uklandregistry.services.generator_service.random.choices', return_value=['Processing']) # status

    # Mock date generation
    fixed_date = date(2024, 2, 1)
    generator_service.random_date = MagicMock(return_value=fixed_date)

    application, app_dict = generator_service.generate_random_application() # No type specified

    mock_app_type_repo.get_all.assert_called_once()
    assert application.application_type_id == SAMPLE_APP_TYPE_ADDITIONAL.id
    assert application.applicants == ['Test Corp Ltd', 'Another Ltd']
    assert application.property_address == '2 Corp Avenue, Industrious, I1 1II'
    assert application.form_used == 'CH1'
    assert application.status == 'Processing'
    assert application.priority == 3
    assert application.lender == 'Mock Lender Inc.' # Check added field
    assert application.loan_amount == 150000 # Check added field
    assert app_dict['application_type'] == SAMPLE_APP_TYPE_ADDITIONAL.name
    assert app_dict['lender'] == 'Mock Lender Inc.'
    assert app_dict['loan_amount'] == 150000

def test_generate_applications_by_type(generator_service, mock_app_repo, mocker):
    """Test generating applications with specific type counts."""
    type_counts = {'First Registration': 2, 'Charge': 1}

    # Mock the generate_random_application to return predictable results
    mock_app_instance = Application(reference='TestRef', application_type_id=1)
    mock_app_dict = {'reference': 'TestRef', 'application_type': 'First Registration'} # Simplified dict
    mock_generate = mocker.patch.object(generator_service, 'generate_random_application', return_value=(mock_app_instance, mock_app_dict))

    app_dicts = generator_service.generate_applications(type_counts=type_counts)

    assert mock_generate.call_count == 3 # 2 + 1
    assert mock_app_repo.add_bulk.call_count == 1
    # Check if add_bulk received a list of 3 Application instances
    assert len(mock_app_repo.add_bulk.call_args[0][0]) == 3
    assert all(isinstance(app, Application) for app in mock_app_repo.add_bulk.call_args[0][0])
    assert len(app_dicts) == 3

def test_generate_applications_total_count(generator_service, mock_app_repo, mocker):
    """Test generating a total number of random applications."""
    total_count = 5

    # Mock generate_random_application
    mock_app_instance = Application(reference='TestRef', application_type_id=1)
    mock_app_dict = {'reference': 'TestRef', 'application_type': 'Random Type'}
    mock_generate = mocker.patch.object(generator_service, 'generate_random_application', return_value=(mock_app_instance, mock_app_dict))

    app_dicts = generator_service.generate_applications(total_count=total_count)

    assert mock_generate.call_count == total_count
    assert mock_app_repo.add_bulk.call_count == 1
    assert len(mock_app_repo.add_bulk.call_args[0][0]) == total_count
    assert len(app_dicts) == total_count

def test_generate_random_application_type_not_found(generator_service, mock_app_type_repo):
    """Test error handling when a specified application type is not found."""
    mock_app_type_repo.get_by_name.return_value = None # Simulate type not found
    app_type_name = "NonExistentType"

    with pytest.raises(ValueError, match=f"Application type '{app_type_name}' not found"):
        generator_service.generate_random_application(app_type_name=app_type_name)

def test_generate_random_application_no_types_in_db(generator_service, mock_app_type_repo):
    """Test error handling when no application types exist in the database for random selection."""
    mock_app_type_repo.get_all.return_value = [] # Simulate no types found

    with pytest.raises(ValueError, match="No application types found in database"):
        generator_service.generate_random_application() # Random selection
