# Resume Evaluation Assistant

An AI-powered application that analyzes resumes (PDF format), extracts key information, and provides an evaluation score with feedback.

## Features

- **PDF Resume Parsing**: Extracts text from PDF resumes
- **Structured Data Extraction**: Identifies and organizes resume content into categories:
  - Personal information (name, contact details)
  - Work experience
  - Education
  - Skills
  - Projects
  - Certifications
- **Automated Scoring**: Calculates a resume quality score (0-100) based on:
  - Experience duration and relevance
  - Education level
  - Skills breadth
  - Project quality
  - Certifications
- **AI Evaluation**: Provides expert feedback on resume quality
- **Interactive UI**: Streamlit-based web interface

## Technologies Used

- **Python 3.9+**
- **Streamlit** - Web application framework
- **Pydantic** - Data validation and settings management
- **PyPDF2** - PDF text extraction
- **Custom AI Agents** - For resume parsing and evaluation
- **Rich** - Console text formatting

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RaoHamzaTariq/AI-Agents-Projects.git
   cd resume-evaluator
   ```
2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .\.venv\Scripts\activate  # Windows
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:

    ```bash
    streamlit run app.py
    ```

2. In your browser:

    - Upload a PDF resume
    - Click "Extract Resume Fields" to parse the resume
    - Click "Get Score & Feedback" for evaluation

## Project Structure

```text
resume-evaluator/
├── app.py                # Streamlit application
├── main.py               # Core business logic
├── schema.py             # Pydantic data models
├── config.py             # Configuration (ignored in git)
├── agents/               # Custom AI agents
│   ├── __init__.py
│   └── tracing.py
├── requirements.txt      # Dependencies
└── README.md            # This file

```

To adjust the scoring weights, modify the `evaluate_resume_score` function in `main.py`:

```python
weights = {
    "experience": 30,  # Adjust these values
    "education": 25,
    "skills": 15,
    "projects": 15,
    "certifications": 15
}
```

## Troubleshooting

**Common Issues:**

1. **PDF text extraction fails**:
   - Ensure the PDF contains selectable text (not scanned images)
   - Try a different PDF library if needed

2. **AI model not responding**:
   - Verify your API key in `config.py`
   - Check your internet connection

3. **Field extraction issues**:
   - Adjust the agent instructions in `resume_agent` (main.py)

## Future Enhancements

- Support for DOCX resume formats
- Integration with job description matching
- Multi-language support
- Enhanced visualizations of resume strengths/weaknesses
- Export evaluation reports (PDF)

## License

MIT License - See [LICENSE](LICENSE) for details.