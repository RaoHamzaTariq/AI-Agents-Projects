from rich import print
from astra.connection import connect_to_database

async def retriever(user_query):
    database = connect_to_database()
    collection = database.get_collection("testing_collection")
    # print(type(collection))
    # Retrieve documents from the collection
    documents = collection.find(sort={"$vectorize": user_query}, limit=3)
    # print(type(documents))
    # print(documents)
    result_text=""
    for doc in documents:
        result_text += f"Found document: {doc['text']}\n"
    return result_text

if __name__ == "__main__":
    retriever("What is the return policy for Nike products?")
    