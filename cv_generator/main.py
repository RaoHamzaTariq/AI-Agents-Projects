from agents import (
    Agent,
    RunContextWrapper,
    RunConfig,
    Runner,
    TResponseInputItem,
    function_tool,
    OpenAIChatCompletionsModel,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents import handoff
from agents.extensions import handoff_filters
from openai import AsyncOpenAI
import asyncio
from dotenv import load_dotenv
from typing import List, Literal, Optional
from dataclasses import dataclass
from pydantic import BaseModel
import os

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

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

# Define a dataclass for cv structure

# @dataclass
class PersonalDetails(BaseModel):
    name: str
    age: int
    role: str

# @dataclass
class ContactInformation(BaseModel):
    email:str
    phone:str
    addresses: list[str]

# @dataclass
class Languages(BaseModel):
    language:str
    proficency: Literal["basic", "conversational", "advanced", "native"]

# @dataclass
class EducationDetails(BaseModel):
    institute_name:str
    degree:str
    passing_year:int

# @dataclass
class WorkExperience(BaseModel):
    company_name:str
    designation:str

# @dataclass
class CV(BaseModel):
    personal_info:PersonalDetails | None
    languages:Languages | None
    education: list[EducationDetails] | None
    experience: list[WorkExperience] | None


@function_tool
def get_cv_data(wrapper:RunContextWrapper[CV]):
    """
    This tool is used to get the data of cv
    """
    try:
        return("CV : ", wrapper.context.model_dump_json())
    except Exception as e:
        print(f"Failed to view user cv: {e}")
        raise

@function_tool
def save_markdown_report(report: str, name:str):
    """Saves the full markdown cv locally for a given cv.
    Use this tool to save the final report once all the details are gathered.
    You must provide the full report as a markdown string.

    Args:
        report (str): Full markdown report
        name (str): Users name
    """
    try:
        with open(f"./reports/{name}_report.md", "w") as f:
            f.write(report)
    except Exception as e:
        print(f"Failed to save report: {e}")
        raise

@function_tool
def save_complete_report(wrapper: RunContextWrapper[CV], cv_name:str):
    """Saves the completed report locally including the PersonalDetails, EducationDetails,WorkExperience,Languages generated.
    Use this tool to save the final report once all the details are gathered.

    Args:
        report_name (str): Report file name (ex: John_Doe_Report)
    """
    try:
        with open(f"./reports/{cv_name}_report.md", "w") as f:
            f.write(wrapper.context.model_dump_json())
    except Exception as e:
        print(f"Failed to save report: {e}")
        raise

@function_tool
def save_personal_details(wrapper: RunContextWrapper[CV], name:str,age:str,role:str) -> bool:
    """Saves the diet plan for the user.

    Args:
        name: Name of the user
        age : Age of user in years
        role: Role of the user
    Returns:
        bool: True if the personal details was saved successfully
        
    Raises:
        Exception: If there was an error saving the diet plan
    """
    try:
        wrapper.context.personal_info = PersonalDetails(
            name=name,
            age=age,
            role=role
        )
        print(f"Saved personal details: {wrapper.context.personal_info.model_dump_json()}")
        return True
    except Exception as e:
        print(f"Failed to save personal details: {e}")
        raise

@function_tool
def save_educational_details(wrapper: RunContextWrapper[CV], institute_name:str,degree:str,passing_year:int) -> bool:
    """Saves the educational details for the user.

    Args:
        institute_name: institure name of user
        degree: name of degree
        passing_year: Passing Year of degree 
    Returns:
        bool: True if the educational details was saved successfully
        
    Raises:
        Exception: If there was an error saving the educational details
    """
    try:
        print("TOols")
        wrapper.context.education.append(EducationDetails(
            institute_name=institute_name,
            degree=degree,
            passing_year=passing_year
        ))
        print(f"Saved educational details: {wrapper.context.education.model_dump_json()}")
        return True
    except Exception as e:
        print(f"Failed to save educational details: {e}")
        raise

@function_tool
def save_experience_details(wrapper: RunContextWrapper[CV], company_name:str,designation:str) -> bool:
    """Saves the experience details for the user.

    Args:
        company_name : company name of user in which they worked
        desgination: designation of the user in that company
    Returns:
        bool: True if the experience details was saved successfully
        
    Raises:
        Exception: If there was an error saving the experience details
    """
    try:
        wrapper.context.experience.append(WorkExperience(
            company_name=company_name,
            designation=designation
        ))
        print(f"Saved experience details: {wrapper.context.experience.model_dump_json()}")
        return True
    except Exception as e:
        print(f"Failed to save experience details: {e}")
        raise

@function_tool
def save_language_details(wrapper: RunContextWrapper[CV], language:str, proficency: Literal["basic", "conversational", "advanced", "native"]) -> bool:
    """Saves the language details for the user.

    Args:
        language:  Language person can speak
        proficieny: Language Proficiency
    Returns:
        bool: True if the Language details was saved successfully
        
    Raises:
        Exception: If there was an error saving the Language details
    """
    try:
        print("Languages TOols")

        wrapper.context.languages=Languages(
            language=language,
            proficency=proficency
        )
        print(f"Saved Language details: {wrapper.context.languages.model_dump_json()}")
        return True
    except Exception as e:
        print(f"Failed to save Language details: {e}")
        raise

@function_tool
def view_current_report(wrapper: RunContextWrapper[CV]):
    """View the current report for the User. Provides context on the PersonalDetails, WorkExperience,EducationDetials and Languages."""
    try:
        return("Current Report: ", wrapper.context.model_dump_json())
    except Exception as e:
        print(f"Failed to view user fitness profile: {e}")
        raise

cv_assistant = Agent(
    name="CV Assistant",
    instructions="You are a personal cv assistant that gathers information on a users personal details and their preferences. You begin by asking a list of questions to get the user personal information. Once you have the information, you save the gathered information using the tool and handover to the Language Agent to get the language. Once the language is know, you handover to the Education Agent to get the education details. Once the education is know, you handover to the Experience Agent to get the experience details. Once all the experience,education,personal, language details is know are built, you explain the cv and get the User's confirmation to save the final report using the tool.",
    model=model,
    tools=[save_complete_report, save_markdown_report,save_personal_details]
)

language_agent = Agent(
    name="Language Agent",
    instructions="You are an expert Language Agent. View the current report to retrieve the Language Details and ask questions to build a languages for the User CV. Once you have the information, you save the gathered information using the tool using the tool save_language_details, then ask for more language if user says yes so add more language otherwise handover back to the CV Assistant.",
    model=model,
    handoffs=[handoff(
        agent=cv_assistant,
        input_filter=handoff_filters.remove_all_tools
    )],
    tools=[view_current_report, save_language_details]
)

educational_agent = Agent(
    name="Educational Agent",
    instructions="You are an expert Educational Agent. View the current report to retrieve the Education Details and ask questions to build a education data for the User CV. Once you have the information, you save the gathered information using the tool using the tool save_education_details, then ask for more education if user says yes so add more education otherwise handover back to the CV Assistant.",
    model=model,
    handoffs=[handoff(
        agent=cv_assistant,
        input_filter=handoff_filters.remove_all_tools
    )],
    tools=[view_current_report, save_educational_details]
)

experience_agent = Agent(
    name="Experience Agent",
    instructions="You are an expert Experience Agent. View the current report to retrieve the Experience Details and ask questions to build a Experience data for the User CV. Once you have the information, you save the gathered information using the tool save_experience_details, then ask for more experience if user says yes so add more experience otherwise handover back to the CV Assistant.",
    model=model,
    handoffs=[handoff(
        agent=cv_assistant,
        input_filter=handoff_filters.remove_all_tools
    )],
    tools=[view_current_report, save_experience_details]
)

cv_assistant.handoffs = [handoff(experience_agent), handoff(educational_agent),handoff(language_agent)]


async def start_chat(primary_agent: Agent, chat: list[TResponseInputItem]):
   
    print("NOTE: Chat started. You can type 'EXIT' to exit the conversation.")
    print("-----------------------------------------")
    cv = CV(personal_info=None,languages=None,education=[],experience=[])
    while True:
               
        
        user_input = input("You: ")
        print("User: ", user_input, "\n")
        
        if user_input == "EXIT":
            print("CV Assistant: Goodbye!", "\n")
            break
        
        chat.append({
            "content": user_input,
            "role" : "user",
            "type": "message"
        })
        
        result = await Runner.run(
            starting_agent=primary_agent, 
            input=chat,
            context=cv,
            run_config=config
        )
        
        chat.clear()
        chat.extend(result.to_input_list())

        print(f"{result.last_agent.name}:", result.final_output, "\n", flush=True)

chat = []
result = asyncio.run(start_chat(cv_assistant, chat))