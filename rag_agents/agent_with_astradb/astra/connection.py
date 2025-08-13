import os
from astrapy import DataAPIClient, Database
from dotenv import load_dotenv

load_dotenv()


def connect_to_database() -> Database:
    """
    Connects to a DataStax Astra database.
    This function retrieves the database endpoint and application token from the
    environment variables `API_ENDPOINT` and `APPLICATION_TOKEN`.

    Returns:
        Database: An instance of the connected database.

    Raises:
        RuntimeError: If the environment variables `API_ENDPOINT` or
        `APPLICATION_TOKEN` are not defined.
    """
    endpoint = os.environ.get("API_ENDPOINT")
    token = os.environ.get("APPLICATION_TOKEN")

    if not token or not endpoint:
        raise RuntimeError(
            "Environment variables API_ENDPOINT and APPLICATION_TOKEN must be defined"
        )

    # Create an instance of the `DataAPIClient` class
    client = DataAPIClient()

    # Get the database specified by your endpoint and provide the token
    database = client.get_database(endpoint, token=token)

    print(f"Connected to database {database.info().name}")

    return database