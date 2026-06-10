import os
import google.generativeai as genai
from dotenv import load_dotenv
from gitlab_tools import get_failed_pipeline, get_job_log, create_issue

load_dotenv()

# Connect to Gemini API (Google Cloud AI)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def diagnose_failure(log_text, pipeline):
    """Send the job log to Gemini and get a diagnosis."""

    prompt = f"""
You are a senior QA engineer and DevOps expert called CI/CD Guardian.

A CI/CD pipeline has failed. Here is the job log:

{log_text[-2000:]}

Please do the following:
1. Identify what exactly failed
2. Explain why it failed in simple terms  
3. Suggest exact steps to fix it

Keep your response clear and concise.
"""

    print("\n=== SENDING LOG TO GEMINI ===")
    response = model.generate_content(prompt)
    diagnosis = response.text
    print("\n=== GEMINI DIAGNOSIS ===")
    print(diagnosis)

    # Auto create GitLab issue with diagnosis
    create_issue(
        title=f"[CI/CD Guardian] Pipeline {pipeline.id} failed on {pipeline.ref}",
        description=f"## Auto-diagnosed by CI/CD Guardian Agent\n\n{diagnosis}"
    )

    return diagnosis


# Run the full agent flow
print("=== CI/CD GUARDIAN AGENT STARTING ===")
pipeline = get_failed_pipeline()
if pipeline:
    log = get_job_log(pipeline)
    if log:
        diagnose_failure(log, pipeline)
def create_issue(title, description):
    """Automatically create a GitLab issue with the diagnosis."""
    issue = project.issues.create({
        "title": title,
        "description": description,
        "labels": ["ci-failure", "auto-generated"],
        "issue_type": "issue"
    })
    print(f"\n=== ISSUE CREATED ===")
    print(f"Title: {title}")
    print(f"URL: {issue.web_url}")
    return issue.web_url1