import os
import google.generativeai as genai
from dotenv import load_dotenv
from gitlab_tools import get_failed_pipeline, get_job_log, create_issue

load_dotenv()

# Connect to Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def diagnose_failure(log_text):
    """Send the job log to Gemini and get a diagnosis."""

    prompt = f"""
You are a senior QA engineer and DevOps expert.

A CI/CD pipeline has failed. Here is the job log:

{log_text[-2000:]}

Please do the following:
1. Identify what exactly failed
2. Explain why it failed in simple terms
3. Suggest how to fix it

Keep your response clear and concise.
"""

    print("\n=== SENDING LOG TO GEMINI ===")
    response = model.generate_content(prompt)
    print("\n=== GEMINI DIAGNOSIS ===")
    print(response.text)
    return response.text


# Run the full flow
pipeline = get_failed_pipeline()
if pipeline:
    log = get_job_log(pipeline)
    if log:
        diagnosis = diagnose_failure(log)
        create_issue(
            title=f"CI Failure — Pipeline {pipeline.id} on {pipeline.ref}",
            description=f"## Auto-diagnosed by CI/CD Guardian Agent\n\n{diagnosis}"
        )