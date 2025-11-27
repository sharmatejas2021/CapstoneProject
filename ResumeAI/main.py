import os
import sys
import asyncio
import argparse
import glob

# ---------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------

# IMPORTANT: Paste Google AI Studio Key

API_KEY = "PASTE_API_KEY"

# ---------------------------------------------------------
# 2. DEPENDENCY CHECK
# ---------------------------------------------------------

try:
    # Set the environment variable automatically if the key is pasted
    
    if "PASTE_API_KEY" not in API_KEY:
        os.environ["GOOGLE_API_KEY"] = API_KEY
        
    # Import Google ADK and PDF libraries
    
    from google.adk.agents import LlmAgent, SequentialAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import InMemoryRunner
    from google.adk.sessions import InMemorySessionService
    from google.adk.tools import FunctionTool
    from pypdf import PdfReader

except ImportError:
    print(" Missing libraries. Please run: pip install -r requirements.txt")
    sys.exit(1)

# ---------------------------------------------------------
# 3. TOOL LAYER
# ---------------------------------------------------------

def pdf_reader_tool(file_path: str) -> str:
    """Reads a real PDF from disk and extracts text."""
    try:
        if not os.path.exists(file_path):
            return "Error: File not found."
        
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Limit text to 15,000 characters to manage token limits
        
        return text[:15000]
    except Exception as e:
        return f"Error reading file: {str(e)}"

# ---------------------------------------------------------
# 4. AGENT LAYER
# ---------------------------------------------------------

def build_pipeline():
    
    # Agent 1: The Screener
    # Scans the resume and makes a PASS/FAIL decision
    
    screener = LlmAgent(
        name="Screener",
        model=Gemini(model="gemini-1.5-flash"),
        instruction="""
        You are an Expert HR Screener.
        1. Use `pdf_reader_tool` to read the resume.
        2. Extract: Candidate Name, Years of Exp, Top 3 Skills.
        3. Evaluate: Must have 3+ years exp AND (Python OR Cloud skills).
        4. Output: A summary and "STATUS: PASS" or "STATUS: FAIL".
        """,
        tools=[FunctionTool(pdf_reader_tool)]
    )

    # Agent 2: The Hiring Manager
    # Reacts to the Screener's output
    
    manager = LlmAgent(
        name="HiringManager",
        model=Gemini(model="gemini-1.5-flash"),
        instruction="""
        You are a Senior Engineering Manager.
        Review the Screener's summary.
        IF FAIL: Write a polite rejection email.
        IF PASS: Write 3 hard, role-specific technical interview questions.
        """
    )

    # Return Sequential Agent (Chains Screener -> Manager)
    
    return SequentialAgent(name="ResumeAI", sub_agents=[screener, manager])

# REQUIRED FOR DEPLOYMENT: Expose the pipeline object globally

pipeline = build_pipeline()

# ---------------------------------------------------------
# 5. EXECUTION LOGIC
# ---------------------------------------------------------

async def process_resume(file_path):
    print(f"\n Processing: {os.path.basename(file_path)}...")
    
    # Initialize the runner with the pipeline and session memory
    
    runner = InMemoryRunner(agent=build_pipeline(), session_service=InMemorySessionService())
    
    # Run the workflow
    
    async for event in runner.run_async(f"Process resume: {file_path}"):
        if event.is_final_response and event.content.parts:
            print(event.content.parts[0].text)
            print("-" * 50)

async def main(target_path):
    if "PASTE_API_KEY" in API_KEY:
        print("Error: Please edit main.py and paste Google API Key.")
        return
    
    print(f" Resume AI Initialized...\n" + "="*50)
    
    # 1. Process specific file
    
    if target_path and os.path.isfile(target_path):
        await process_resume(target_path)
    
    # 2. Process specific folder
    
    elif target_path and os.path.isdir(target_path):
        pdfs = glob.glob(os.path.join(target_path, "*.pdf"))
        for pdf in pdfs: await process_resume(pdf)
    
    # 3. Auto-scan current folder
    
    else:
        print(" Scanning current folder for PDFs...")
        pdfs = glob.glob("*.pdf")
        if not pdfs:
            print(" No PDF files found. Please drag a resume into this folder.")
            return
        for pdf in pdfs: await process_resume(pdf)
            
    print("\n All jobs complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume AI Batch Processor")
    parser.add_argument("path", nargs="?", help="Optional: Specific file or folder path")
    args = parser.parse_args()
    asyncio.run(main(args.path))