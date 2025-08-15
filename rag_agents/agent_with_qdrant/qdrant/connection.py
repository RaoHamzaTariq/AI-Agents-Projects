import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.models import VectorParams, Distance

load_dotenv()


def connect_to_database():
    """
    Connects to a Qdrant Vector database.
    This function retrieves the database endpoint and application token from the
    environment variables `QDRANT_ENDPOINT` and `QDRANT_API_KEY`.

    Returns:
        Database: An instance of the connected database.

    Raises:
        RuntimeError: If the environment variables `QDRANT_ENDPOINT` or
        `QDRANT_API_KEY` are not defined.
    """
    endpoint = os.environ.get("QDRANT_ENDPOINT")
    key = os.environ.get("QDRANT_API_KEY")

    if not key or not endpoint:
        raise RuntimeError(
            "Environment variables QDRANT_ENDPOINT and QDRANT_API_KEY must be defined"
        )
    
    try:
        # Create an instance of the `QdrantClient` class
        client = QdrantClient(
            url = endpoint,
            api_key = key,
        )
        print("Connected to Qdrant")
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")

    return client


    

if __name__ == "__main__":
    client = connect_to_database()