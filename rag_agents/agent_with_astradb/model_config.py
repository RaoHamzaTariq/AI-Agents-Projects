from agents import OpenAIChatCompletionsModel,RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

client = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    # tracing_disabled=True
)