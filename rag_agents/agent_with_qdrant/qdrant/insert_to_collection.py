import json

import qdrant_client
from connection import connect_to_database
from rich import print
import numpy as np
from qdrant_client.models import PointStruct
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant

def main() -> None:
    try:
        client = connect_to_database()

        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        data_file_path = "./documents/docs.json"

        # Read the JSON file and parse it into a JSON array
        with open(data_file_path, "r", encoding="utf8") as file:
            json_data = json.load(file)

        # Assemble the documents to insert:
        # # Insert the data
        # Convert to list of document dicts
        docs_to_insert = [
            {"id": id_val, "text": doc_text}
            for id_val, doc_text in zip(json_data["ids"], json_data["documents"])
        ]

        texts = [doc["text"] for doc in docs_to_insert]
        metadatas = [{"id": doc["id"], "text": doc["text"]} for doc in docs_to_insert]


        vector_store = Qdrant(
        client=client,
        collection_name="testing_collection",
        embeddings=embedding_model
        )

        vector_store.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        
        print("✅ Data inserted into Qdrant successfully!")
    except Exception as e:
        print(f"❌ Error inserting data into Qdrant: {e}")

if __name__ == "__main__":
    main()