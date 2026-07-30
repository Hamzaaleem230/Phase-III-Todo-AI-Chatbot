# Implementation Plan: PHASE III: TODO AI CHATBOT

**Branch**: `001-todo-ai-chatbot` | **Date**: 2026-06-30 | **Spec**: [specs/001-todo-ai-chatbot/spec.md](specs/001-todo-ai-chatbot/spec.md)
**Input**: Feature specification from `/specs/001-todo-ai-chatbot/spec.md`

## Summary

This plan outlines the implementation of an AI-powered chatbot for the existing Todo application. The primary goal is to enable logged-in users to interact with their todo list using natural language (Create, List, Update, Delete todos) without modifying existing Phase I (Auth) or Phase II (Todo CRUD) functionalities. The technical approach involves integrating an LLM for intent classification and entity extraction on the backend, extending the FastAPI backend with new, isolated API routes, and developing a dedicated chat UI on the Next.js frontend.

## Technical Context

**Language/Version**:
- Backend: Python 3 (FastAPI, SQLModel, Alembic)
- Frontend: TypeScript/JavaScript (Next.js)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Alembic, PostgreSQL (Neon), LLM client library (e.g., Google Generative AI for Gemini or Anthropic for Claude)
- Frontend: Next.js, React
**Storage**: PostgreSQL (Neon) for existing Todos and a new table for Chat History.
**Testing**:
- Backend: pytest
- Frontend: (Implied Jest/React Testing Library for Next.js)
**Target Platform**:
- Backend: Linux server (containerized)
- Frontend: Web browser
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: End-to-end latency for processing a user message and returning a response is under 2 seconds for 90% of requests (SC-005).
**Constraints**:
- Strictly additive changes only; DO NOT modify, delete, or refactor existing Phase I/II code.
- DO NOT rename existing folders, files, routes, tables, or environment variables.
- DO NOT touch existing authentication logic, user model, or todo CRUD directly; interact only through existing, stable APIs/logic.
- LLM interaction is abstracted and isolated within the backend.
**Scale/Scope**: Individual logged-in users interacting with their personal todo lists via a chatbot.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **SAFETY FIRST**: Adhered to by strictly enforcing additive changes and not overwriting existing code.
-   **MINIMALISM**: Plan focuses solely on Phase III objectives, avoiding over-engineering or unnecessary abstractions.
-   **BACKEND FIRST**: AI logic and intent parsing will reside in the backend; the frontend will solely consume new API endpoints.
-   **TRACEABILITY**: The design will ensure clear separation between chat parsing, intent detection, and existing todo execution logic.
-   **STEP-BY-STEP EXECUTION**: This plan itself follows a structured, step-by-step approach.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── tasks.py
│   │       └── chat.py          # NEW: Chat API routes (under /api/v1/chat)
│   ├── core/
│   ├── crud/
│   ├── db/
│   │   ├── database.py
│   │   └── models.py            # Existing models
│   │   └── chat.py              # NEW: Chat history model
│   ├── dependencies/
│   ├── models/
│   │   └── chat.py              # NEW: Chat model definition
│   ├── routers/
│   │   └── chat.py              # NEW: Chat routing logic
│   ├── schemas/
│   │   └── chat.py              # NEW: Chat message Pydantic schemas
│   └── services/
│       └── ai/                  # NEW: AI service abstraction layer
│           ├── base.py
│           ├── gemini.py        # NEW: Gemini/Claude integration
│           └── claude.py        # NEW: Claude integration
└── tests/                       # Existing backend tests

frontend/
├── src/
│   ├── app/
│   │   ├── login/
│   │   ├── profile/
│   │   ├── signup/
│   │   ├── tasks/
│   │   └── chat/                # NEW: Chat UI page (e.g., page.tsx)
│   ├── components/
│   │   ├── Forms.tsx
│   │   ├── Navbar.tsx
│   │   ├── ProtectedRoute.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskList.tsx
│   │   ├── UserMenu.tsx
│   │   └── ChatComponent.tsx    # NEW: Chat message display and input
│   └── lib/
└── tests/                       # Existing frontend tests
```

**Structure Decision**: The plan adopts Option 2 (Web application) and extends the existing `backend/app/` and `frontend/src/app/` structures with new, isolated modules and files for Phase III functionality. This ensures clear separation of concerns and adheres to the "additive changes only" constraint.

## Complexity Tracking

## Phases

### Phase 0: Outline & Research

**Goal**: Address unknowns and gather necessary information for detailed design.

1.  **Research Tasks**:
    *   **LLM Provider Integration**: Research the specific client libraries and API best practices for integrating the chosen LLM (Gemini or equivalent) into the FastAPI backend. Determine authentication, rate limits, and error handling mechanisms.
    *   **LLM Output Schema**: Define a robust and extensible structured JSON output schema that the LLM will provide, encompassing intent classification (CREATE_TODO, LIST_TODOS, UPDATE_TODO, DELETE_TODO) and entity extraction (e.g., `todo_title`, `due_date`, `status`, `target_id`). This schema will serve as the contract between the LLM and the backend's business logic.
    *   **LLM Prompt Engineering**: Research effective prompt engineering strategies to guide the LLM to consistently produce the desired JSON output, handle ambiguous inputs, and manage conversational context.
    *   **Abstracting LLM Interaction**: Evaluate different patterns for abstracting the LLM interaction (e.g., Strategy pattern, Factory pattern) to allow for easy swapping of AI providers in the future without impacting core logic.

2.  **Consolidate Findings in `research.md`**:
    *   **Decision**: [To be determined post-research, e.g., "Use Google Generative AI Python SDK for Gemini integration, employing a Strategy pattern for LLM abstraction."]
    *   **Rationale**: [To be determined post-research, explaining why certain choices were made (e.g., "SDK provides robust error handling, Strategy pattern offers flexibility for future AI model changes.")]
    *   **Alternatives considered**: [To be determined post-research, e.g., "Direct HTTP calls to LLM API (rejected due to less convenience and higher error proneness), hardcoding LLM logic (rejected due to lack of extensibility)."]

**Output**: `specs/001-todo-ai-chatbot/research.md` (fully resolved unknowns)

### Phase 1: Design & Contracts

**Prerequisites**: `research.md` is complete and all Phase 0 research questions are resolved.

1.  **Extract Entities & Data Model (`data-model.md`)**:
    *   **ChatHistory**:
        *   **Purpose**: Stores a record of user messages and AI responses for conversational context and audit.
        *   **Attributes**:
            *   `id` (UUID, Primary Key)
            *   `user_id` (UUID, Foreign Key to existing User model)
            *   `message_content` (Text, User's input)
            *   `response_content` (Text, AI's generated response)
            *   `timestamp` (DateTime, when the message/response occurred)
            *   `intent_classified` (String, e.g., "CREATE_TODO", "LIST_TODOS", "UNSURE")
            *   `extracted_entities` (JSON, structured data parsed from LLM, e.g., `{"title": "Buy milk", "due_date": "tomorrow"}`)
        *   **Relationships**: Many-to-one with User (a user can have many chat history entries).
    *   **Todo (Existing)**: The existing Todo model will be used without modification. No new fields are added to the Todo model itself.

2.  **Generate API Contracts (`contracts/`)**:
    *   **Endpoint**: `POST /api/v1/chat/send-message`
        *   **Description**: Sends a user message to the chatbot, processes it via LLM, performs todo operations, and returns a natural language response.
        *   **Authentication**: Requires authenticated user (via existing token/session mechanism).
        *   **Request Body (`schemas/chat.py` - `ChatMessageRequest`)**:
            *   `message`: String (User's natural language input)
        *   **Response Body (`schemas/chat.py` - `ChatMessageResponse`)**:
            *   `response`: String (AI's natural language response)
            *   `action_taken`: Optional[String] (e.g., "TODO_CREATED", "TODO_LISTED", "NO_ACTION")
            *   `action_details`: Optional[JSON] (details of the action taken, e.g., `{"todo_id": "...", "title": "..."}`)
        *   **Error Responses**:
            *   `401 Unauthorized`: If user is not authenticated.
            *   `400 Bad Request`: Invalid input or LLM processing error.
            *   `500 Internal Server Error`: Unexpected backend/LLM issues.

3.  **Quickstart Guide (`quickstart.md`)**:
    *   Will include steps for setting up LLM API keys (e.g., `GEMINI_API_KEY` in `.env`).
    *   Instructions for running database migrations for the new `ChatHistory` table.
    *   Guidance on deploying the extended backend and frontend.

4.  **Agent Context Update**:
    *   Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini` to inform the agent about new models/services/dependencies.

**Output**: `specs/001-todo-ai-chatbot/data-model.md`, `specs/001-todo-ai-chatbot/contracts/chat_api.yaml` (or equivalent), `specs/001-todo-ai-chatbot/quickstart.md`

## Risks and Guardrails (Phase III Specific)

*   **Risk**: LLM output inconsistency (malformed JSON, incorrect intent/entity).
    *   **Guardrail**: Robust validation of LLM's structured output on the backend. Fallback mechanisms to prompt user for clarification or generic error messages.
*   **Risk**: Accidental modification of existing Phase I/II code.
    *   **Guardrail**: Strict adherence to "additive changes only". Code reviews focused on diffs against existing files. New features developed in clearly segregated modules/files.
*   **Risk**: Performance degradation due to LLM latency.
    *   **Guardrail**: Implement asynchronous API calls for LLM integration. Frontend can display loading indicators. Explore caching strategies for common LLM responses if feasible.
*   **Risk**: Security vulnerabilities through LLM (e.g., prompt injection leading to unintended DB operations).
    *   **Guardrail**: LLM ONLY provides intent and entities; NO direct DB operations. All actions are routed through existing, validated backend business logic. Input sanitization before LLM processing.
*   **Risk**: Feature creep, expanding beyond Phase III scope.
    *   **Guardrail**: Strict adherence to the spec's defined capabilities and non-goals. Any new ideas must go through a formal proposal process.