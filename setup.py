from setuptools import setup, find_packages

setup(
    name="uklandregistry",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary>=2.9.9",
        "sqlalchemy>=2.0.27",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "uklandregistry=uklandregistry.cli:run_cli",
        ],
    },
    author="LandRegistry", # TODO: Update with actual author name
    author_email="your.email@example.com", # TODO: Update with actual author email
    description="UK Land Registry application data generator",
    keywords="land registry, data generation, testing",
    python_requires=">=3.7",
)
