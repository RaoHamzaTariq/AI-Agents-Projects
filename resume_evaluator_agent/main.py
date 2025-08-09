
from datetime import datetime
import pandas as pd
from PyPDF2 import PdfReader
from config import model
from schema import ResumeModel, EvaluationScoreModel
from agents import Agent, Runner , RunContextWrapper,ModelSettings
from agents.tracing import trace
from datetime import datetime
from rich import print
from io import BytesIO
import re



# --- PDF TEXT EXTRACTION ---
# This function now accepts a file-like object and uses pypdf
def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    """Extracts text from a PDF file object using pypdf."""
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text with pypdf: {e}")
        return ""
    return text


# --- SCORING FUNCTIONS ---
def evaluate_resume_score(resume: ResumeModel) -> float:
    """
    Evaluates a resume to produce a general quality score from 0 to 100.
    """
    total_score = 0
    weights = {
        "experience": 30,
        "education": 25,
        "skills": 15,
        "projects": 15,
        "certifications": 15
    }

    # --- 1. Experience Length (30 points) ---
    experience_years = 0
    for exp in resume.experience:
        if exp.start_date and exp.end_date:
            try:
                start_year_match = re.search(r'\d{4}', exp.start_date)
                end_year_str = exp.end_date.lower()
                end_year_match = re.search(r'\d{4}', end_year_str)
                if start_year_match:
                    start_year = int(start_year_match.group())
                    if end_year_str == 'present':
                        end_year = datetime.now().year
                    elif end_year_match:
                        end_year = int(end_year_match.group())
                    else:
                        continue
                    experience_years += end_year - start_year
            except (ValueError, AttributeError):
                continue
    
    max_experience_years = 10
    experience_score_ratio = min(experience_years / max_experience_years, 1.0)
    total_score += experience_score_ratio * weights["experience"]

    # --- 2. Education (25 points) ---
    education_score_ratio = 0.0
    if resume.education:
        degree_values = {
            "phd": 1.0, "doctor": 1.0,
            "master": 0.8,
            "bachelor": 0.6,
            "associate": 0.4
        }
        highest_degree_score = 0.0
        for edu in resume.education:
            degree_text = edu.degree.lower() if edu.degree else ""
            for key, value in degree_values.items():
                if key in degree_text:
                    highest_degree_score = max(highest_degree_score, value)
        education_score_ratio = highest_degree_score
    total_score += education_score_ratio * weights["education"]

    # --- 3. Number of Skills (15 points) ---
    max_skills_for_score = 20
    if resume.skills:
        skills_score_ratio = min(len(resume.skills) / max_skills_for_score, 1.0)
        total_score += skills_score_ratio * weights["skills"]

    # --- 4. Number of Projects (15 points) ---
    max_projects_for_score = 5
    if resume.projects:
        projects_score_ratio = min(len(resume.projects) / max_projects_for_score, 1.0)
        total_score += projects_score_ratio * weights["projects"]

    # --- 5. Number of Certifications (15 points) ---
    max_certs_for_score = 3
    if resume.certifications:
        certs_score_ratio = min(len(resume.certifications) / max_certs_for_score, 1.0)
        total_score += certs_score_ratio * weights["certifications"]
    
    return round(total_score)


# --- AGENT DEFINITIONS ---

resume_agent = Agent(
    model=model,
	name="Resume Agent",
	instructions= """
    You are an expert resume parsing agent. Your primary goal is to meticulously
    analyze the provided resume text and extract all relevant information, structuring it
    precisely into a JSON object that strictly adheres to the provided 'ResumeModel' Pydantic schema.

    The resume text will be given as a single string. Your task is to identify and populate
    the following fields:
    - **name**: The full name of the applicant.
    - **role**: The desired job title or role.
    - **email**: The primary email address.
    - **phone**: The primary phone number.
    - **other_links**: A list of URLs for professional profiles (e.g., LinkedIn, GitHub, personal portfolio).
    - **skills**: A list of technical and soft skills.
    - **experience**: A list of work experiences, each with a job title, company, start date, and end date.
    - **education**: A list of educational qualifications, each with a degree, institution, and graduation year.
    - **projects**: A list of personal or professional projects, each with a title and a brief description.
    - **languages**: A list of languages the applicant speaks.
    - **certifications**: A list of professional certifications or licenses.

    For any field that is not present or cannot be found in the resume, you must return
    an empty list for list-based fields or `None` for string/integer fields, as specified in the model.
    """,
	output_type=ResumeModel
)

score_agent = Agent(
    name="Resume Evaluation Agent",
    model =model,
    output_type=EvaluationScoreModel,
    model_settings=ModelSettings(
        temperatue=0.2,
        
    )
)

def dynamic_score_agent_instruction(run_context: RunContextWrapper[None], agent: Agent, score: float
) -> str:
    return f"""
    You are a resume evaluation agent designed to evaluate the score of the resume. Currently according to the system, 
    the evaluation score is {score} but you have evaluate the score.

    Criteria of Evaluation:

    Total Max Score: 100
    Weights:
    1. Experience: 40
    2. Skills: 20
    3. Projects: 20
    4. Certifications: 20

    You have to analyze proper resume and provide the evaluation score based on the criteria mentioned above.
    Also keep in mind the system's evaluation criteria and weights. Also consider the system evaluation score which is {score} but you can adjust it based on your analysis. Don't fully rely on the system's score.
"""



async def extract_resume_fields_from_pdf(pdf_file: BytesIO) -> ResumeModel | None:
    """
    Orchestrates the resume parsing part of the workflow.
    """
    try:
        resume_text = extract_text_from_pdf(pdf_file)
        if not resume_text:
            return "Could not extract text from the PDF.", None
        print("Extracted Resume Text:",resume_text[:500])  # Print first 500 characters for debugging
        print("--- Starting Resume Parsing ---")
        parsed_resume_output = await Runner.run(
            resume_agent,
            f"Here is the resume text for the document: {resume_text}"
        )
        resume_data = parsed_resume_output.final_output
        print("--- Parsed Resume Data ---")
        print(resume_data)
        return resume_data

    except Exception as e:
        print("An error occurred during extraction:", e)
        return None


async def evaluate_and_score_resume(resume_data: ResumeModel) -> EvaluationScoreModel | None:
    """
    Orchestrates the scoring part of the workflow.
    """
    try:
        # Step 1: Calculate the system-based evaluation score
        system_score = evaluate_resume_score(resume_data)
        print(f"--- System-Calculated Score: {system_score} ---")

        # Step 2: Use the AI score agent for a final, expert evaluation
        print("--- Starting Expert Evaluation ---")
        score_agent.instructions = dynamic_score_agent_instruction(
            run_context=RunContextWrapper[None],
            agent=score_agent,
            score=system_score
        )

        combined_prompt=f"Evaluate the resume score for the following resume: {resume_data.model_dump_json()}"

        ai_resume_score_output = await Runner.run(score_agent, combined_prompt)
        final_evaluation = ai_resume_score_output.final_output

        print("--- Final Expert Evaluation ---")
        print(final_evaluation)

        return final_evaluation

    except Exception as e:
        print("An error occurred during evaluation:", e)
        return None

# if __name__ == "__main__":
#     try:
#         import asyncio
#         asyncio.run(run_agent())
#     except Exception as e:
#         print("Error occurred:", e)

        
    # with trace(workflow_name="Resume Evaluation Workflow",group_id="resume_evaluation"):