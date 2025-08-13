from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from astra.connection import connect_to_database
from rich import print
import json

PDF_PATH = "./documents/BI_Structure_Nike_Ecommerce_Policy.pdf"

pages = PyPDFLoader(PDF_PATH).load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(pages)

docs = [doc.page_content for doc in chunks]
ids = [f"chunk_{i}" for i in range(len(docs))]


with open("documents/docs.json", "w", encoding="utf8") as file:
    json.dump({"documents": docs, "ids": ids}, file)
