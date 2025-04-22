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
WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
if WEATHER_API_KEY is None:
    raise ValueError("WEATHER_API_KEY environment variable not set.")


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

# Tools

@dataclass
class WeatherInfo:
   temperature: float
   feels_like: float
   humidity: int
   description: str
   wind_speed: float
   pressure: int
   location_name: str
   visibility: Optional[int] = None

@function_tool
def get_weather(city_name: str) -> str:
   """Get the current weather for a specified location using OpenWeatherMap API.

   Args:
       city_name (str): The name of the city to get the weather for.
   """

   # Build URL with parameters
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name.capitalize()}&appid={WEATHER_API_KEY}"

   try:
       response = requests.get(url)
       response.raise_for_status()
       data = response.json()

       # Extract weather data from the response
       weather_info = WeatherInfo(
           temperature=data["main"]["temp"],
           feels_like=data["main"]["feels_like"],
           humidity=data["main"]["humidity"],
           description=data["weather"][0]["description"],
           wind_speed=data["wind"]["speed"],
           pressure=data["main"]["pressure"],
           location_name=data["name"],
           visibility=data.get("visibility")
       )

       # Build the response string
       weather_report = f"""
       Weather in {weather_info.location_name}:
       - Temperature: {weather_info.temperature- 273.15}°C (feels like {weather_info.feels_like- 273.15}°C)
       - Conditions: {weather_info.description}
       - Humidity: {weather_info.humidity}%
       - Wind speed: {weather_info.wind_speed*3.6} km/h
       - Pressure: {weather_info.pressure} hPa
       """
       return weather_report

   except requests.exceptions.RequestException as e:
       return f"Error fetching weather data: {str(e)}"



# Create a weather assistant
weather_agent = Agent(
   name="Weather Assistant",
   instructions="""You are a weather assistant that can provide current weather information.
  
   When asked about weather, use the get_weather tool to fetch accurate data.
   If the user doesn't specify a city name and there might be ambiguity,
   ask for clarification (e.g., Paris, Karachi).
  
   Provide friendly commentary along with the weather data, such as clothing suggestions
   or activity recommendations based on the conditions.
   """,
   tools=[get_weather]
)

async def weather_assistant(user_input:str):
  
   # Run the agent with the user's input
    response = await Runner.run(starting_agent=weather_agent,input=user_input,run_config=config)
    return response

# print(asyncio.run(weather_assistant("Tell me the weather in Karachi"))) # Karachi, Pakistan