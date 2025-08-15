from langchain_google_genai import GoogleGenerativeAIEmbeddings
from rich import print
from qdrant.connection import connect_to_database

def retriever(user_query):
    # 1. Connect to Qdrant
    client = connect_to_database()

    # 2. Create the embeddings model
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # 4. Get query vector from Gemini
    query_vector = embedding_model.embed_query(user_query)

    # 5. Search in Qdrant
    search_results = client.search(
        collection_name="testing_collection",
        query_vector=query_vector,
        limit=3  # top 3 most similar documents
    )
    
    # 6. Print results
    for hit in search_results:
        print(f"Score: {hit.score}")
        print(f"Payload: {hit.payload}")
        print(f"ID: {hit.id}")
        print(f"Vector: {hit.vector}")
        print("------")

    result_text=""
    for hit in search_results:
        result_text += f"Found document: {hit.payload['page_content']}\n"
    return result_text

if __name__ == "__main__":
    retriever("What is the return policy for Nike products?")
    