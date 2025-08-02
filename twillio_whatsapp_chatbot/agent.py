from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_default_openai_client,
    function_tool,
    set_tracing_disabled,
    RunConfig
)
import os
import asyncio
from dotenv import load_dotenv
import random

import requests


load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")


client = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# set_tracing_disabled(disabled=True)
# set_default_openai_client(client)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)




# Create a weather assistant
joke_agent = Agent(
   name="WhatsApp Agent",
   instructions="""
    You are Whatsapp Agent which is designed to tell jokes
"""
)

async def joke_assistant(user_input:str):
  
   # Run the agent with the user's input
    response = await Runner.run(starting_agent=joke_agent,input=user_input,run_config=config)
    return response

# print(asyncio.run(joke_assistant("Tell me the joke about dog"))) # Karachi, Pakistan