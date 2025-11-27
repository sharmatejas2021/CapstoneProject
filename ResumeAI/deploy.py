import os
import subprocess
import sys

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# IMPORTANT: Paste Google Cloud Project ID

PROJECT_ID = "GOOGLE_CLOUD_PROJECT_ID" 
REGION = "us-central1"
ENTRYPOINT = "main:pipeline"

def run_command(command):
    """Runs a shell command and prints the output."""
    try:
        print(f"Executing: {command}...")
        subprocess.check_call(command, shell=True)
        print("Done.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error details: {e}")
        sys.exit(1)

def main():
    print("="*50)
    print(" Resume AI - Google Cloud Deployment Wrapper")
    print("="*50)

    # 1. Set the Google Cloud Project
    
    print(f"Setting project to: {PROJECT_ID}")
    run_command(f"gcloud config set project {PROJECT_ID}")

    # 2. Deploy to Vertex AI Agent Engine
    
    print("Deploying to Agent Engine...")
    deploy_cmd = (
        f"adk deploy agent_engine "
        f"--project {PROJECT_ID} "
        f"--region {REGION} "
        f"--entrypoint {ENTRYPOINT}"
    )
    run_command(deploy_cmd)

    print("Deployment process finished successfully.")

if __name__ == "__main__":
    if PROJECT_ID == "GOOGLE_CLOUD_PROJECT_ID":
        print("Error: Please edit deploy.py and paste Google Cloud Project ID .")
        sys.exit(1)
        
    main()