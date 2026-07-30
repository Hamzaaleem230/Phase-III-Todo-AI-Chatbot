---
id: 0001
title: Initial Constitution Ratification
stage: constitution
date: 2026-06-30
surface: agent
model: gemini-cli-agent
feature: none
branch: main
user: syeda
command: /sp.constitution
labels: ["constitution", "initial-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

/sp.constitution

You are working on an existing, partially completed project named:

PHASE III TODO AI CHATBOT

==============================
CRITICAL CONTEXT (READ FIRST)
==============================

This project is a continuation of Hackathon II.

IMPORTANT:
- Phase I and Phase II logic, structure, and intent MUST be preserved.
- Backend infrastructure is ALREADY SET UP and WORKING.
- Database migrations have ALREADY BEEN RUN using Alembic.
- FastAPI backend is RUNNING successfully.
- Health endpoint returns 200 OK.
- Database tables for todo and chat ALREADY EXIST.

You MUST NOT:
- Delete any existing files
- Rename existing files or folders
- Refactor working backend infrastructure
- Change database connection logic
- Modify Alembic history or migration files
- Replace authentication, config, or DB setup
- Remove or rewrite existing endpoints unless explicitly instructed

You MAY ONLY:
- ADD new files
- ADD new endpoints
- ADD new services or modules
- EXTEND existing code carefully without breaking it

==============================
PROJECT STRUCTURE (CURRENT)
==============================

Root:
- backend/
  - app/
    - main.py (WORKING)
    - core/config.py (WORKING, ENV LOADED)
    - db/database.py (WORKING)
    - models/, routers/, services/ (partially present)
  - alembic/ (MIGRATIONS APPLIED)
  - venv/

- frontend/
  - Next.js project
  - Vercel config exists
  - package.json may be incomplete or generated later

==============================
PHASE III OBJECTIVE
==============================

Build an AI-powered Todo Chatbot that:

- Understands natural language input
- Can CREATE, UPDATE, DELETE, and LIST todos via chat
- Uses LLM reasoning (Gemini / Claude via CLI routing)
- Maps user intent → structured todo actions
- Stores todos in the existing database
- Logs chat history appropriately
- Exposes clean API endpoints for frontend use

This is NOT a greenfield project.
This is an EXTENSION of an already working system.

==============================
DESIGN PRINCIPLES (MANDATORY)
==============================

1. SAFETY FIRST
   - Never assume missing context
   - Never overwrite existing code
   - Prefer additive changes only

2. MINIMALISM
   - Write only the code required for Phase III
   - No over-engineering
   - No unnecessary abstractions

3. BACKEND FIRST
   - AI logic and intent parsing lives in backend
   - Frontend only calls APIs

4. TRACEABILITY
   - Each AI decision must be explainable
   - Clear separation between:
     - Chat parsing
     - Intent detection
     - Todo execution

5. STEP-BY-STEP EXECUTION
   - Plan before coding
   - Tasks before implementation
   - One concern per file

==============================
LLM USAGE RULES
==============================

- Gemini / Claude may be used ONLY for:
  - Intent classification
  - Structured JSON output
  - Natural language understanding

- LLMs must NOT:
  - Directly execute DB operations
  - Bypass backend validation
  - Generate uncontrolled SQL

==============================
SUCCESS CRITERIA
==============================

Phase III is considered COMPLETE when:

- A user can type:
  "Add a todo to buy milk tomorrow"
- The system:
  - Understands intent
  - Extracts structured data
  - Saves todo to DB
  - Responds with confirmation

And similarly for:
- List todos
- Update todo
- Delete todo

==============================
FINAL RULE
==============================

If ANY requirement is ambiguous:
STOP and ask for clarification.

DO NOT GUESS.
DO NOT MODIFY EXISTING WORKING CODE.

## Response snapshot

Updated the project constitution, including core principles, LLM usage rules, and success criteria. Version set to 1.0.0. Provided a list of files for manual follow-up.

## Outcome

- ✅ Impact: Constitution document created/updated with initial project guidelines.
- 🧪 Tests: N/A
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Review other templates for alignment with the constitution.
- 🧠 Reflection: Successfully parsed the user's input to populate the constitution template. Ensured all mandated sections were included and placeholders were filled. Provided clear instructions for follow-up actions regarding dependent files.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A