from connection import connect_to_database
from qdrant_client.models import VectorParams, Distance

def main() -> None:
    client = connect_to_database()

    try:

        collection_name = "testing_collection"
        if not client.collection_exists(collection_name=collection_name):
            # Create a new collection with specified vector parameters
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768,distance=Distance.COSINE)
            )

        print(f"Created collection {collection_name}")
    except Exception as e:
        print(f"Error creating collection {collection_name}: {e}")

if __name__ == "__main__":
    main()