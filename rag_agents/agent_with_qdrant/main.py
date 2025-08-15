from qdrant.retriever import retriever
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
        result = retriever(prompt)
        return result
    except Exception as e:
        return str(e)

agent = Agent(
    name="RAG Agent",
    instructions="""
    You are the General Queries Agent for an e-commerce website. Your role is to handle all customer inquiries that don't fall under order tracking, product recommendations, or order placement, including:

    1. Company information
    2. Return/refund policies
    3. Shipping policies
    4. Payment options
    5. Account management questions
    6. Website technical help
    7. General customer service

    Always use tool 'rag_tool'
    Be polite, professional, and helpful. Provide clear, accurate information from the company's knowledge base. If a question requires accessing customer-specific data, use the provided functions. For complex issues you can't resolve, offer to escalate to human support

    If the query are irrelevent so politely inform the user that their question falls outside the scope of your expertise and suggest they contact customer support for further assistance.
    Also handle the greeting type queries polielty

    for example User say: Hi 
    assistant : How can i help you?

    for example : what is your return policy?
    Now use rag tool because this type of info is avaible in documents
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
