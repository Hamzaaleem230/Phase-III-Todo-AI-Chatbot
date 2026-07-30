<!-- Sync Impact Report:
Version Change: 0.0.0 -> 1.0.0
Modified Principles: (none - initial population)
Added Sections: LLM Usage Rules, Success Criteria
Removed Sections: (none)
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/sp.adr.toml ⚠ pending
- .specify/templates/commands/sp.analyze.toml ⚠ pending
- .specify/templates/commands/sp.checklist.toml ⚠ pending
- .specify/templates/commands/sp.clarify.toml ⚠ pending
- .specify/templates/commands/sp.constitution.toml ⚠ pending
- .specify/templates/commands/sp.git.commit_pr.toml ⚠ pending
- .specify/templates/commands/sp.implement.toml ⚠ pending
- .specify/templates/commands/sp.phr.toml ⚠ pending
- .specify/templates/commands/sp.plan.toml ⚠ pending
- .specify/templates/commands/sp.reverse-engineer.toml ⚠ pending
- .specify/templates/commands/sp.specify.toml ⚠ pending
- .specify/templates/commands/sp.tasks.toml ⚠ pending
- .specify/templates/commands/sp.taskstoissues.toml ⚠ pending
- README.md ⚠ pending
- docs/ENVIRONMENT_SETUP.md ⚠ pending
Follow-up TODOs: Ensure alignment of all dependent templates and documentation with the updated constitution.
-->
# PHASE III TODO AI CHATBOT Constitution

## Core Principles

### SAFETY FIRST
Never assume missing context.
Never overwrite existing code.
Prefer additive changes only.

### MINIMALISM
Write only the code required for Phase III.
No over-engineering.
No unnecessary abstractions.

### BACKEND FIRST
AI logic and intent parsing lives in backend.
Frontend only calls APIs.

### TRACEABILITY
Each AI decision must be explainable.
Clear separation between:
- Chat parsing
- Intent detection
- Todo execution

### STEP-BY-STEP EXECUTION
Plan before coding.
Tasks before implementation.
One concern per file.

## LLM Usage Rules

- Gemini / Claude may be used ONLY for:
  - Intent classification
  - Structured JSON output
  - Natural language understanding

- LLMs must NOT:
  - Directly execute DB operations
  - Bypass backend validation
  - Generate uncontrolled SQL

## Success Criteria

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

## Governance

If ANY requirement is ambiguous:
STOP and ask for clarification.
DO NOT GUESS.
DO NOT MODIFY EXISTING WORKING CODE.

Amendments to this constitution require documentation, approval, and a migration plan.

**Version**: 1.0.0 | **Ratified**: 2026-06-30 | **Last Amended**: 2026-06-30
