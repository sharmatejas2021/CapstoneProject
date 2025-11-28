# CapstoneProject

5-Day AI Agents Intensive Course with Google

---

## ❓Problem Statement

In the modern enterprise, posting a single open engineering role can attract hundreds of applicants in a matter of hours. For Hiring Managers and HR teams, this volume creates a significant bottleneck that standard keyword filters cannot solve.

The current manual process suffers from three critical flaws:-

- Cognitive Load: Recruiters spend an average of only 6-7 seconds per resume, often leading to fatigue and oversight.

- Context Switching: If a candidate passes the initial screen, the hiring manager must then spend 20-30 minutes re-reading the resume to draft unique, relevant technical interview questions.

- Candidate Ghosting: Due to volume, rejected candidates often receive no feedback.

---

## 💯 Solution

Agents are the ideal solution because recruitment is a multi-step cognitive process, not a single prediction task. A standard LLM can summarize a resume, but it cannot act like a hiring manager.

Thus, Resume AI is a fully automated recruitment pipeline built with the **Google Agents Development Kit (ADK)** and powered by `gemini-1.5-flash`. Instead of using a single large prompt to do everything, the system mimics a real-world HR team structure by chaining specialized AI agents.

The system ingests raw PDF resumes and performs a sophisticated two-step workflow:-

1. **Screening**: A "Screener" agent reads the document and validates requirements (e.g., "Must have 3+ years of experience in Python").

2. **Response**: A "Hiring Manager" agent reacts to the Screener's findings to generate interview questions or rejection emails.

---

## ⚙️ Architecture

The project implements a Sequential Agent pattern using the `google.adk` library and `gemini-1.5-flash` model powering the agents. This architecture ensures that the "Hiring Manager" agent never sees a raw resume; it only acts on the structured, synthesized data provided by the "Screener," simulating a real corporate workflow.

### 📌 Key Components

#### 1. Sequential Multi-Agent Architecture

##### Agent 1: The Screener (The Logic Engine)

- Model: `gemini-1.5-flash`

- Role: **Expert HR Screener**

- Function: The Screener agent autonomously calls the `pdf_reader_tool` to ingest data. It then applies strict boolean logic based on the requirements to determine a `✅PASS` or `❌FAIL` status.

##### Agent 2: The Hiring Manager (The Generative Engine)

- Model: `gemini-1.5-flash`

- Role: **Senior Engineering Manager**

- Function: The Hiring agent receives status from the Screener agent and reacts on the basis of status:-
                
1. **✅PASS**: Uses the refined context to generate hard, role-specific technical interview questions.

2. **❌FAIL**: Drafts polite rejection email, ensuring positive candidate experience.

#### 2. Custom Tool (PDF Ingestion)

LLMs cannot natively read binary files from a local disk. To solve this a custom tool `pdf_reader_tool` is built using the `pypdf` library. This function is wrapped as a `FunctionTool` and exposed to the Screener Agent. It allows the agent to autonomously read the file path provided by the user or scan the current folder for resume PDFs, extract the raw text and truncate it to 15,000 characters to manage token limits effectively.

#### 3. Context Engineering & State Management

A major challenge in long-context tasks is "distraction". To solve this **Context Compaction** is implemented.

The Screener Agent does not pass the entire raw PDF text to the next agent; instead, it extracts and standardizes the data and the `InMemorySessionService` manages this state, passing only the clean, high-signal data to the Hiring agent. This ensures the final output is based on verified facts rather than noise found in the original document.

#### 4. Deployment

The agent is designed for enterprise scalability. It is configured for deployment to the **Google Cloud Vertex AI Agent Engine** using a custom deployment wrapper `deploy.py` that utilizes `adk deploy` command.

<img width="2816" height="1536" alt="Gemini_Generated_Image_x7a19fx7a19fx7a1" src="https://github.com/user-attachments/assets/729007f0-4358-4667-8d32-49f14132e651" />

---

## 🚀 Instructions for Setup

### System Requirements

- Python 3.10+

- Google AI Studio API Key

- Google Cloud Project ID (Cloud Deployment)

### Installing the ResumeAI Project Folder

#### 1. Cloning Github Repository

Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux),enter the following command:

```
git clone https://github.com/sharmatejas2021/CapstoneProject.git
```

#### 2. Manual Installation

- Install the ResumeAI Project Folder

### Local Run

- Navigate Project Directory (Enter file path if installed manually)

```
cd ResumeAI
```

- Install Dependencies

```
pip install -r requirements.txt
```

- Edit `main.py` and enter your `Google AI Studio API Key` in the **Configuration** section

  `API_KEY = "PASTE_API_KEY"`

- Run `main.py` ( Add resume PDFs to the project directory manually or enter the file path of a specific file or folder in the terminal after running the program file `main.py`)

```
python main.py
```

❗The requirements for the job role, text to be extracted and also the no. of interview questions can be edited in the **Agent Layer**.

### Cloud Deployment (Google Cloud Vertex AI Agent Engine)

- Navigate Project Directory (Enter file path if installed manually)

```
cd ResumeAI
```

- Edit `deploy.py` and enter your `Google Cloud Project ID` in the **Configuration** section

  `PROJECT_ID = "GOOGLE_CLOUD_PROJECT_ID" `

- Run `deploy.py`

<img width="2816" height="1536" alt="Gemini_Generated_Image_xaurltxaurltxaur" src="https://github.com/user-attachments/assets/c7538238-f88f-42d5-b6ca-77b057ceb927" />








