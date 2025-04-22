# agent.py

from agents import (
    Agent,
    RunContextWrapper,
    RunConfig,
    Runner,
    function_tool,
    OpenAIChatCompletionsModel,
    set_default_openai_client,
    set_tracing_disabled,
)
from openai import AsyncOpenAI
import asyncio
from dotenv import load_dotenv
from typing import Optional
from dataclasses import dataclass
from emails import send_email as send_real_email
import os

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL = os.getenv("EMAIL")

if EMAIL is None:
    raise ValueError("EMAIL environment variable is not set.")
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")
if EMAIL_PASSWORD is None:
    raise ValueError("EMAIL_PASSWORD environment variable is not set.")

# Set up the Gemini API-compatible client
client = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Wrap into RunConfig
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
)

# Define a dataclass for email structure
@dataclass
class EmailInfo:
    subject: str
    sender: str
    recipient: str
    body: str

# Tool function to send email
@function_tool
def send_email_tool(
    subject: str,
    recipient: str,
    body: str
) -> str:
    """
    Send an email using Gmail SMTP server.
    :param subject: Subject of the email
    :param recipient: Recipient's email address
    :param body: Body of the email
    :return: Status message indicating success or failure
    """
    return send_real_email(
        sender_email=EMAIL,
        password=EMAIL_PASSWORD,
        to_email=recipient,
        subject=subject,
        body=body
    )

with open('demo_email.txt', 'r') as file:
    demo_email_content = file.read()

# Register the Email Agent with a more comprehensive description
email_agent = Agent(
    tools=[send_email_tool],
    instructions=f"You are an Email Agent capable of sending emails directly through Gmail. The agent will handle sending the email. This agent does not support CC or BCC, so it sends an email to a single recipient only.If user doesn't provide a subject, use subject related to email as the default. DEMO FILE {demo_email_content}",
    model=model,
    name="Email Agent"
)

# Function to run the email agent asynchronously with user input
async def run_email_agent(user_input: str) -> str:
    try: 
        result = await Runner.run(
            starting_agent=email_agent,
            input=user_input,
            run_config=config
        )
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage:
# Assuming you want to send an email requesting sick leave
# print(asyncio.run(run_email_agent("Send an email to sick leave to my manager yasapid216@f5url.com so please approve my sick leave")))
