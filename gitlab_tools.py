import os
import gitlab
from dotenv import load_dotenv

load_dotenv()

# Connect to GitLab
gl = gitlab.Gitlab(
    url=os.getenv("GITLAB_URL"),
    private_token=os.getenv("GITLAB_TOKEN")
)

# Open your project
project = gl.projects.get(os.getenv("GITLAB_PROJECT_ID"))


def get_failed_pipeline():
    """Find the most recent failed pipeline."""
    pipelines = project.pipelines.list(status="failed", per_page=1)
    if not pipelines:
        print("No failed pipelines found.")
        return None
    pipeline = pipelines[0]
    print(f"Found failed pipeline ID: {pipeline.id}")
    print(f"Branch: {pipeline.ref}")
    print(f"URL: {pipeline.web_url}")
    return pipeline


def get_job_log(pipeline):
    """Get the error log from the failed job inside that pipeline."""
    # Get ALL jobs first, then filter manually
    jobs = pipeline.jobs.list()
    
    print(f"\nAll jobs in pipeline:")
    for job in jobs:
        print(f"  Job name: {job.name}, Status: {job.status}")
    
    # Find any job that is not successful
    failed_job = None
    for job in jobs:
        if job.status != "success":
            failed_job = job
            break
    
    if not failed_job:
        print("No failed jobs found.")
        return None
    
    print(f"\nReading log from job: {failed_job.name}")
    job = project.jobs.get(failed_job.id)
    log = job.trace()
    log_text = log.decode("utf-8")
    print("\n=== JOB LOG (last 2000 chars) ===")
    print(log_text[-2000:])
    return log_text

# Run it
pipeline = get_failed_pipeline()
if pipeline:
    get_job_log(pipeline)

def create_issue(title, description):
    """Automatically create a GitLab issue with the diagnosis."""
    issue = project.issues.create({
        "title": title,
        "description": description,
        "labels": ["ci-failure", "auto-generated"]
    })
    print(f"\n=== ISSUE CREATED ===")
    print(f"Title: {title}")
    print(f"URL: {issue.web_url}")
    return issue.web_url