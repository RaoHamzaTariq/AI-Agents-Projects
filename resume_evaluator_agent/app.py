import streamlit as st
from main import extract_resume_fields_from_pdf,evaluate_and_score_resume
from io import BytesIO
import asyncio
from schema import ResumeModel, EvaluationScoreModel

# Set page configuration
st.set_page_config(
    page_title="Resume Evaluation Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Resume Evaluation Assistant")
st.markdown("Upload a PDF resume to get an automated score and AI-powered feedback.")

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file  = None
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'evaluation_resume' not in st.session_state:
    st.session_state.evaluation_resume = None

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

# --- Step 1: Extract Resume Fields ---
st.header("1. Extract Resume Fields")
if st.session_state.uploaded_file:
    if st.button("Extract Resume Fields"):
        st.session_state.resume_data = None
        st.session_state.evaluation_resume = None
        
        # Pass the file content as a BytesIO object directly
        pdf_content = BytesIO(st.session_state.uploaded_file.getvalue())
        with st.spinner("Extracting fields from resume..."):
            try:
                resume_data = asyncio.run(extract_resume_fields_from_pdf(pdf_content))
                st.session_state.resume_data = resume_data
                st.success("Resume fields extracted successfully!")
            except Exception as e:
                st.error(f"Error extracting resume fields: {e}")            
else:
    st.info("Please upload a PDF file to begin.")

# Display extracted resume data if available
if st.session_state.resume_data and isinstance(st.session_state.resume_data, ResumeModel):
    st.markdown("---")
    st.header("Resume Details")
    st.subheader(st.session_state.resume_data.name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Role:** {st.session_state.resume_data.role}")
    with col2:
        st.markdown(f"**Email:** {st.session_state.resume_data.email}")
    with col3:
        st.markdown(f"**Phone:** {st.session_state.resume_data.phone}")

    st.markdown(f"**Links:** {', '.join(st.session_state.resume_data.other_links)}")

    with st.expander("Show detailed resume sections", expanded=True):
        st.subheader("Experience")
        if st.session_state.resume_data.experience:
            st.table([{"Job Title": exp.job_title, "Company": exp.company, "Start Date": exp.start_date, "End Date": exp.end_date} for exp in st.session_state.resume_data.experience])
        else:
            st.info("No experience found.")
        
        st.subheader("Education")
        if st.session_state.resume_data.education:
            st.table([{"Degree": edu.degree, "Institution": edu.institution, "Start Year": edu.start_year, "End Year": edu.end_year} for edu in st.session_state.resume_data.education])
        else:
            st.info("No education found.")
        
        st.subheader("Skills")
        st.write(", ".join(st.session_state.resume_data.skills))
        
        st.subheader("Projects")
        st.write(", ".join(st.session_state.resume_data.projects))
        
        st.subheader("Certifications")
        st.write(", ".join(st.session_state.resume_data.certifications))

# --- Step 2: Get Evaluation Score ---
st.markdown("---")
st.header("2. Get Evaluation Score")
if st.session_state.resume_data:
    if st.button("Get Score & Feedback"):
        with st.spinner("Generating scores and feedback..."):
            try:
                evaluation=  asyncio.run(evaluate_and_score_resume(st.session_state.resume_data))
                if evaluation is not None:
                    st.session_state.evaluation_resume = evaluation
                st.success("Evaluation complete!")
            except Exception as e:
                st.error(f"Error generating scores and feedback: {e}")
        

else:
    st.info("Please extract resume fields first to get a score.")

# Display scores and feedback if available
if st.session_state.evaluation_resume:
    st.markdown("---")
    st.header("Evaluation Scores")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("System Score", f"{st.session_state.evaluation_resume.system_score}/100", delta_color="off")
    with col2:
        st.metric("AI Expert Score", f"{st.session_state.evaluation_resume.score}/100", delta_color="off")
    
    

    st.markdown("---")
    st.header("AI Expert Review")
    st.info(st.session_state.evaluation_resume.feedback)
