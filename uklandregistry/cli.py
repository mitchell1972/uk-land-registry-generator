"""
Command-line interface for the UK Land Registry application data generator.
"""
import argparse
import logging
from .services.database_service import DatabaseService
from .services.generator_service import GeneratorService
from .data.application_types import get_application_type_names

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate UK Land Registry application data and store in PostgreSQL"
    )
    
    # Database options
    parser.add_argument('--db-uri', dest='db_uri', 
                       help='PostgreSQL connection URI')
    parser.add_argument('--reset-db', dest='reset_db', action='store_true',
                       help='Reset the database (drop all tables and recreate)')
    
    # Output options
    parser.add_argument('--sample-json', dest='sample_json', 
                       help='Save sample as JSON to specified file')
    parser.add_argument('--print-samples', dest='print_samples', type=int, default=5, 
                       help='Number of samples to print (default: 5)')
    
    # Generation options
    app_type_names = get_application_type_names()
    for app_type in app_type_names:
        arg_name = app_type.replace('/', '').replace(' ', '-').lower()
        parser.add_argument(f'--{arg_name}', type=int, default=0,
                         help=f'Number of {app_type} applications to generate')
    
    parser.add_argument('--random-count', type=int, default=20,
                       help='Number of random applications to generate if no specific types requested')
    
    return parser.parse_args()


def run_cli():
    """Run the command-line interface"""
    args = parse_args()
    
    try:
        # Initialize database
        db_service = DatabaseService()
        
        if args.reset_db:
            logger.info("Resetting database...")
            if not db_service.reset_database():
                logger.error("Failed to reset database")
                return 1
        else:
            logger.info("Initializing database...")
            if not db_service.initialize_database():
                logger.error("Failed to initialize database")
                return 1
        
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
        generator = GeneratorService()
        
        if total_specified > 0:
            logger.info(f"Generating {total_specified} applications with specific counts")
            samples = generator.generate_applications(type_counts=type_counts)
        else:
            logger.info(f"Generating {args.random_count} random applications")
            samples = generator.generate_applications(total_count=args.random_count)
        
        # Print samples
        if args.print_samples > 0:
            print_count = min(args.print_samples, len(samples))
            print(f"\n=== SAMPLE UK LAND REGISTRY APPLICATIONS ({print_count}) ===\n")
            for sample in samples[:print_count]:
                print(generator.format_application_for_display(sample))
                print()
        
        # Save to JSON if requested
        if args.sample_json:
            if generator.save_to_json(samples, args.sample_json):
                logger.info(f"Successfully saved samples to {args.sample_json}")
            else:
                logger.error(f"Failed to save samples to {args.sample_json}")
        
        # Clean up
        generator.close()
        
        logger.info("Done")
        return 0
    
    except Exception as e:
        logger.exception(f"Error running CLI: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_cli()) 