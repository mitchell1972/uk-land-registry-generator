# UK Land Registry Application Data Generator

## Simple Explanation

This tool creates realistic sample data for UK Land Registry applications - the kind of applications people submit when buying, selling, or changing something about their property ownership in England and Wales.

### How It Works (Simply Explained)

1. **What it does**: The tool creates fake but realistic property applications with details like:
   - Who's applying (names of people or companies)
   - What property they're dealing with (addresses)
   - What type of application it is (first registration, mortgage, etc.)
   - When it was submitted
   - Current status (pending, completed, etc.)

2. **Where it stores data**: 
   - The data goes into a PostgreSQL database (running in Docker, which is like a lightweight container)
   - It can also save data as JSON files for easy sharing

3. **Under the hood**:
   - It has pre-defined templates for different types of Land Registry applications
   - It randomly generates details (names, addresses, dates) within realistic parameters
   - It follows the rules of what information belongs with each application type

### Quick Start Guide

1. **Setup** (one-time only):
   
   Install the package:
   `pip install -e .`
   
   Start the database:
   `docker-compose up -d`

2. **Basic usage** - generate 20 random applications:
   `uklandregistry`

3. **Generate specific types of applications**:
   `uklandregistry --first-registrations 10 --transfers-of-ownership 5`
   
   This creates 10 "First Registration" applications and 5 "Transfer of Ownership" applications.

4. **Looking at Your Data**:
   - Open http://localhost:5050 in your browser
   - Login with email: `admin@example.com`, password: `admin`
   - Connect to the database using the details in the "Accessing the Database" section below

Now, on to the more detailed documentation:

## Overview

This project provides a robust framework for generating realistic test data for UK Land Registry applications and storing it in a PostgreSQL database. It is designed for developers, testers, and data scientists working with property registration systems who need large volumes of realistic sample data to validate functionality, performance, or analytics processes.

The generator creates detailed applications that follow the structure and business rules of HM Land Registry in England and Wales, with appropriate metadata, status tracking, and relationships.

## Features

- **Comprehensive Data Generation**: Create realistic UK Land Registry applications with all required fields and relationships
- **PostgreSQL Integration**: Store generated data directly in a PostgreSQL database using SQLAlchemy ORM
- **Precise Control**: Specify exact counts for each application type to create balanced test datasets
- **Docker Support**: Run the database infrastructure in Docker containers for easy setup and teardown
- **JSON Export**: Export generated data to JSON files for integration with other systems
- **Clean Architecture**: Well-structured code following repository pattern and separation of concerns
- **Flexible Configuration**: Configure database connections and other settings via environment variables
- **Command-line Interface**: Generate data through both a CLI tool and Python API
- **Detailed Data Model**: Includes both core and additional application types with appropriate fields

## Architecture

The project follows a clean architecture approach with clear separation of concerns:

```
uklandregistry/
├── models/          # Database entity definitions
├── repositories/    # Data access layer for persistence operations
├── services/        # Business logic and data generation
├── data/            # Static reference data (application types)
├── utils/           # Helper functions and sample data
├── cli.py           # Command-line interface
└── config.py        # Configuration management

scripts/             # Entry point scripts
```

### Key Components

- **Models**: Define the database schema using SQLAlchemy ORM
- **Repositories**: Provide data access operations for each entity type
- **Services**: Implement business logic and data generation
- **Config**: Manage configuration settings from environment variables
- **CLI**: Command-line interface for data generation

## Prerequisites

- **Docker and Docker Compose**: Required for running PostgreSQL and pgAdmin containers
- **Python 3.7+**: Required for running the application
- **pip**: Required for installing dependencies
- **PostgreSQL client** (optional): For direct database access

## Installation

### 1. Clone the Repository

`git clone https://github.com/yourusername/uk-land-registry-generator.git`
`cd uk-land-registry-generator`

### 2. Install the Package

Install the package in development mode to enable immediate updates during development:

`pip install -e .`

This will install all required dependencies, including:
- SQLAlchemy (ORM for database operations)
- psycopg2-binary (PostgreSQL driver)
- python-dotenv (Environment variable management)

### 3. Start the Database Services

`docker-compose up -d`

This will start:
- PostgreSQL database on port 5433
- pgAdmin web interface on port 5050

### 4. Verify Installation

Check that the services are running properly:

`docker ps`

You should see two containers running: `land_registry_db` and `land_registry_pgadmin`.

## Configuration

The application can be configured using environment variables or a `.env` file in the project root:

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_USER` | Database username | landregistry |
| `DB_PASSWORD` | Database password | landregistry |
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | 5433 |
| `DB_NAME` | Database name | land_registry |
| `LOG_LEVEL` | Logging level | INFO |

Example `.env` file:

```
DB_USER=landregistry
DB_PASSWORD=landregistry
DB_HOST=localhost
DB_PORT=5433
DB_NAME=land_registry
LOG_LEVEL=INFO
```

## Usage

### Command-line Interface

The package provides a command-line tool `uklandregistry` for generating data.

#### Basic Usage

Generate 20 random applications (default behavior):

`uklandregistry`

#### Specify Counts per Application Type

Generate specific numbers of each application type:

`uklandregistry --first-registrations 10 --transfers-of-ownership 5 --leases-and-lease-extensions 3 --chargesmortgages 7 --restrictionsnotices 4`

#### Reset Database

Reset the database (drop all tables and recreate) before generating data:

`uklandregistry --reset-db --random-count 50`

#### Save to JSON

Save the generated data to a JSON file:

`uklandregistry --first-registrations 10 --transfers-of-ownership 5 --sample-json output.json`

#### Control Output Verbosity

Control how many sample records are printed to console:

`uklandregistry --random-count 100 --print-samples 0`  # No printing to console
`uklandregistry --random-count 100 --print-samples 10`  # Print 10 samples

### Python API

The package also provides a Python API for more programmatic control:

```python
from uklandregistry.services.database_service import DatabaseService
from uklandregistry.services.generator_service import GeneratorService

# Initialize the database
db_service = DatabaseService()
db_service.initialize_database()  # Creates tables if they don't exist

# Generate applications with the GeneratorService
generator = GeneratorService()

# Generate 10 random applications
random_samples = generator.generate_applications(total_count=10)

# Generate specific counts by type
type_counts = {
    "First Registrations": 5,
    "Transfers of Ownership": 3,
    "Charges/Mortgages": 7,
    "Adverse Possession": 2
}
specific_samples = generator.generate_applications(type_counts=type_counts)

# Save to JSON
generator.save_to_json(specific_samples, "output.json")

# Format and display a sample
print(generator.format_application_for_display(specific_samples[0]))

# Clean up
generator.close()
```

### Application Types

The system supports the following application types:

#### Core Application Types
- First Registrations
- Transfers of Ownership
- Leases and Lease Extensions
- Charges/Mortgages
- Restrictions/Notices
- Title Corrections

#### Additional Application Types
- Assents
- Cautions Against First Registration
- Adverse Possession
- Change of Name or Address
- Severance of Joint Tenancy
- Official Copies and Searches
- Easements and Rights of Way
- Discharge of Restrictive Covenants
- Death of Proprietor
- Equitable Charges

Each application type has specific forms and may have type-specific fields (e.g., mortgage applications include lender and loan amount details).

## Accessing the Database

### Using pgAdmin

1. Open http://localhost:5050 in your browser
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin`
3. Add a server connection:
   - Name: Land Registry
   - Host: `host.docker.internal` (or your Docker host IP)
   - Port: `5433`
   - Database: `land_registry`
   - Username: `landregistry`
   - Password: `landregistry`

### Direct SQL Access

To connect directly to the database using `psql`:

`psql -h localhost -p 5433 -U landregistry -d land_registry`

## Data Model

### Main Entities

#### ApplicationType
Represents the different types of Land Registry applications:
- `id`: Primary key
- `category`: 'core' or 'additional'
- `name`: Name of the application type
- `description`: Detailed description
- `forms`: JSON array of forms associated with this type

#### Application
Represents an individual Land Registry application:
- `id`: Primary key
- `reference`: Unique reference (e.g., "LR123456X")
- `application_type_id`: Foreign key to ApplicationType
- `property_address`: Address of the property
- `applicants`: JSON array of applicant names
- `submission_date`: Date submitted
- `expected_completion_date`: Expected completion date
- `status`: Current status (Pending, Processing, etc.)
- `priority`: Priority level (1-5)
- `form_used`: The form used for this application
- Type-specific fields:
  - `lender`: For mortgage applications
  - `loan_amount`: For mortgage applications
  - `reason_for_correction`: For title correction applications

## Troubleshooting

### Common Issues

#### Port Conflicts
If you have another PostgreSQL instance running on port 5432, the default port has been changed to 5433 in this application. If you still encounter port conflicts, you can modify the `docker-compose.yml` file to use a different port.

#### Database Connection Issues
If you encounter database connection issues:
- Ensure Docker containers are running: `docker ps`
- Check the database logs: `docker logs land_registry_db`
- Verify your connection settings in `.env` file or environment variables

#### Session Errors
The application uses SQLAlchemy sessions. If you encounter session-related errors:
- Make sure you properly close sessions using `generator.close()`
- For complex scripts, consider using session contexts to ensure proper cleanup

### Docker Container Management

List running containers:
`docker ps`

Stop containers:
`docker-compose down`

Reset containers and remove volumes:
`docker-compose down -v`
`docker-compose up -d`

## Performance Considerations

For large data generation jobs:
- Use the `--print-samples 0` option to avoid printing to console, which can slow down processing
- Consider using batch inserts by breaking up large generation jobs into smaller chunks
- For very large datasets (millions of records), consider running the script on a machine with adequate memory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- HM Land Registry for their public documentation about application types and processes
- SQLAlchemy for the powerful ORM capabilities
- Docker for container technology that simplifies database setup
