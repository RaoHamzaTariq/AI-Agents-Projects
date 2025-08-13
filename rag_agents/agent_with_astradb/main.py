from astra.retriever import retriever
from agents import function_tool, Runner, Agent
from model_config import model
from fastapi import FastAPI

app = FastAPI()

@function_tool
async def rag_tool(prompt:str)->str:
    """
    Retrieves a response from the chromadb based on the input prompt.
    Args:
    prompt (str): The input prompt to be used for retrieval.
    Returns:
    str: The retrieved response from the chromadb.
    """
    try:
        result = await retriever(prompt)
        return result
    except Exception as e:
        return str(e)

agent = Agent(
    name="RAG Agent",
    instructions="""
    You are a retrieval-augmented generation (RAG) agent. Your task is to retrieve relevant documents from a database and use them to generate a response to the user's query.
    """,
    tools=[rag_tool],
    model=model
)


async def main(user_query):
    result = await Runner.run(agent, user_query)
    return result.final_output

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Agent API"}

@app.post("/query")
async def query(user_query: str):
    result = await main(user_query)
    return {"response": result}
