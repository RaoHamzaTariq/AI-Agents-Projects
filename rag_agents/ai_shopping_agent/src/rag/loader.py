from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
import os
from pprint import pprint

CHROMA_DIR = "./chroma"
PDF_PATH = "./src/documents/BI_Structure_Nike_Ecommerce_Policy.pdf"

client = chromadb.Client(Settings(is_persistent=True, persist_directory=CHROMA_DIR))
collection = client.get_or_create_collection(name="Nike_Ecommerce")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

pages = PyPDFLoader(PDF_PATH).load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(pages)

docs = [doc.page_content for doc in chunks]
ids = [f"chunk_{i}" for i in range(len(docs))]
collection.upsert(documents=docs, ids=ids)

if __name__ == "__main__":
    query = "What is the warranty duration for Nike products?"
    results = collection.query(query_texts=[query], n_results=1)
    print("Sample answer:", results["documents"][0])

# No need to call client.persist(); new versions auto-persist.
