import json
from astra.connection import connect_to_database
from astrapy.data_types import DataAPIDate
from rich import print

def main() -> None:
    database = connect_to_database()

    collection = database.get_collection("testing_collection")

    data_file_path = "./documents/docs.json"

    # Read the JSON file and parse it into a JSON array
    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    # Assemble the documents to insert:
    # # Insert the data
    # Convert to list of document dicts
    docs_to_insert = [
        {"id": id_val, "text": doc_text, "$vectorize": doc_text}
        for id_val, doc_text in zip(json_data["ids"], json_data["documents"])
]


    inserted = collection.insert_many(documents=docs_to_insert)

    print(f"Inserted {len(inserted.inserted_ids)} documents.")
    

if __name__ == "__main__":
    main()