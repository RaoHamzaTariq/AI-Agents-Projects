from config.model import model
from agents import Agent,Runner
from multi_agents.general_faqs_agent import general_faqs_agent
from multi_agents.product_recommendation_agent import product_recommendation_agent
import asyncio

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are the Triage Agent for an e-commerce website. Your role is to analyze the user's query and determine which specialized agent should handle it. You must quickly identify whether the user is asking about:

    1. Product recommendations (route to Product Recommendation Agent)
    2. General questions about the company, policies, or website (route to General Queries Agent)

    Do not attempt to answer the query yourself. Simply identify the most appropriate agent and handoff the query to that agent.

    For greeting, response politely without handoff
    """,
    model=model,
    handoffs=[
        product_recommendation_agent,
        general_faqs_agent
    ]
)

