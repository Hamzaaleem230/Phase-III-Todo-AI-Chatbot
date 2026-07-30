# Implementation Tasks: PHASE III: TODO AI CHATBOT

**Feature Branch**: `001-todo-ai-chatbot`  
**Date**: 2026-06-30  
**Spec**: [specs/001-todo-ai-chatbot/spec.md](specs/001-todo-ai-chatbot/spec.md)  
**Plan**: [specs/001-todo-ai-chatbot/plan.md](specs/001-todo-ai-chatbot/plan.md)

This document outlines the step-by-step implementation tasks for the AI-powered Todo Chatbot feature. Tasks are grouped by user story and ordered to facilitate incremental development and testing.

## Dependency Graph (User Story Completion Order)

All user stories are designed to be largely independent in their core logic once foundational elements are in place. However, the order of implementation below follows a logical progression from creation to viewing to modification/deletion.

1.  **Foundational Backend & Setup** (Prerequisite for all stories)
2.  **User Story 1 - Create Todo** (P1)
3.  **User Story 2 - List Todos** (P1)
4.  **User Story 3 - Update Todo** (P2)
5.  **User Story 4 - Delete Todo** (P2)
6.  **Frontend Integration & Polish** (Integrates all backend stories)

## Parallel Execution Opportunities

Once the "Foundational Backend & Setup" is complete, the development of Frontend UI components can begin in parallel with the implementation of individual backend User Stories, as long as the backend API contract is stable.

*   Backend: User Story 1 (Create Todo) -> User Story 2 (List Todos) -> User Story 3 (Update Todo) -> User Story 4 (Delete Todo)
*   Frontend: Chat UI Development can run in parallel, integrating with the `/api/v1/chat/send-message` endpoint as it becomes available.

## Implementation Strategy

An MVP (Minimum Viable Product) for the chatbot would encompass the "Foundational Backend & Setup" tasks and the "User Story 1 - Create Todo" (P1) and "User Story 2 - List Todos" (P1) backend implementation, followed by the basic "Frontend Integration" to allow users to interact with these core functionalities. Subsequent stories can then be delivered incrementally.

---

### Phase 1: Foundational Backend & Setup (Shared)

**Why this phase exists**: These tasks establish the core infrastructure and abstractions required for all AI chatbot functionalities, ensuring a solid, extensible foundation before implementing specific user stories.

**Tasks**:

-   [X] T001 Add `google-generativeai` to `backend/requirements.txt`
    *   *Why this task exists*: Installs the necessary Python SDK for interacting with Google Gemini.
-   [X] T002 Update `backend/.env.example` with `GEMINI_API_KEY` placeholder
    *   *Why this task exists*: Documents the required environment variable for LLM authentication.
-   [X] T003 Create `backend/app/services/ai/base.py` for abstract LLM service interface (NEW FILE)
    *   *Why this task exists*: Defines the contract for LLM services, enabling extensibility and decoupling from concrete implementations.
-   [X] T004 Create `backend/app/services/ai/gemini.py` implementing `GeminiLLMService` from `base.py` (NEW FILE)
    *   *Why this task exists*: Provides the concrete implementation for interacting with the Google Gemini API.
-   [X] T005 Create `backend/app/models/chat.py` for `ChatHistory` SQLModel (NEW FILE)
    *   *Why this task exists*: Defines the database schema for storing chatbot interactions.
-   [X] T006 Create `backend/app/schemas/chat.py` for `ChatMessageRequest` and `ChatMessageResponse` Pydantic schemas (NEW FILE)
    *   *Why this task exists*: Defines the data structures for API request and response bodies for chat messages.
-   [X] T007 Generate Alembic migration for the `ChatHistory` table (NEW FILE in `backend/alembic/versions/`)
    *   *Why this task exists*: Creates the necessary database table to persist chat history.
-   [X] T008 Apply Alembic migration to create `chat_history` table (COMMAND)
    *   *Why this task exists*: Executes the database schema change.
-   [X] T009 Create `backend/app/crud/chat.py` for `ChatHistory` CRUD operations (NEW FILE)
    *   *Why this task exists*: Provides standardized methods for interacting with the `ChatHistory` database model.

---

### Phase 2: User Story 1 - Create Todo (P1)

**Story Goal**: A user can successfully create a new todo item by sending a natural language message to the chatbot.  
**Independent Test**: A user sends "Add a todo to buy groceries tomorrow", and the system confirms creation, then the new todo appears in their list.

**Tasks**:

-   [X] T010 [US1] Create `backend/app/services/chat.py` with `process_chat_message` function (NEW FILE)
    *   *Why this task exists*: Centralizes the logic for LLM interaction, intent parsing, and dispatching to existing todo CRUD.
-   [X] T011 [US1] Implement LLM call and structured JSON parsing within `process_chat_message`
    *   *Why this task exists*: Integrates the Gemini LLM to interpret user messages and extract structured data.
-   [X] T011a [US1] Implement a `try-except` block around the LLM call and JSON parsing in `backend/app/services/chat.py` to handle API errors, timeouts, and malformed JSON responses from the LLM.
    *   *Why this task exists*: To gracefully handle failures in the LLM interaction and prevent crashes.
-   [ ] T011b [US1] Add a validation function in `backend/app/services/chat.py` to sanitize and validate entities extracted from the LLM's JSON output.
    *   *Why this task exists*: To ensure data integrity and prevent security vulnerabilities before using extracted entities in business logic.
-   [X] T011c [US1] Add logic in `backend/app/services/chat.py` to check for "UNKNOWN" or low-confidence intents from the LLM and return a user-friendly clarification prompt.
    *   *Why this task exists*: To handle ambiguous user inputs gracefully, improving user experience.
-   [X] T012 [US1] Add logic to `process_chat_message` to handle `CREATE_TODO` intent, calling `crud.todos.create_todo` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Connects LLM intent to existing todo creation functionality.
-   [X] T013 [US1] Implement saving of user message and AI response to `ChatHistory` within `process_chat_message` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Persists chat interactions for traceability.
-   [X] T014 [US1] Create `backend/app/routers/chat.py` with `POST /api/v1/chat/send-message` endpoint (NEW FILE)
    *   *Why this task exists*: Exposes the chatbot functionality via a new, isolated API route.
-   [X] T015 [US1] Add dependency to `backend/app/main.py` to include `chat.py` router (MODIFICATION to `backend/app/main.py`)
    *   *Why this task exists*: Registers the new chat API routes with the FastAPI application.
-   [X] T016 [US1] Secure `POST /api/v1/chat/send-message` endpoint using existing authentication dependencies (MODIFICATION to `backend/app/routers/chat.py`)
    *   *Why this task exists*: Ensures only authenticated users can interact with the chatbot.
-   [X] T016a [US1] Create a custom exception handler in `backend/app/routers/chat.py` to catch specific application errors (e.g., `LLMProcessingError`, `ValidationError`) and return user-friendly, standardized error messages.
    *   *Why this task exists*: To provide clear and actionable error feedback to the user, improving usability.

---

### Phase 3: User Story 2 - List Todos (P1)

**Story Goal**: A user can successfully view their current todo items by sending a natural language message to the chatbot.  
**Independent Test**: A user sends "Show my todos", and the system responds with a formatted list of their todos.

**Tasks**:

-   [X] T017 [US2] Enhance `process_chat_message` to handle `LIST_TODOS` intent, calling `crud.todos.get_user_todos` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Extends chatbot's capability to retrieve and display user's todos.
-   [X] T018 [US2] Format the list of todos into a natural language response within `process_chat_message` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Ensures a user-friendly output for listing todos.

---

### Phase 4: User Story 3 - Update Todo (P2)

**Story Goal**: A user can successfully modify an existing todo item's details or status using natural language.  
**Independent Test**: A user sends "Mark the milk todo as done", and the system confirms the update, then the todo's status is changed.

**Tasks**:

-   [ ] T019 [US3] Enhance `process_chat_message` to handle `UPDATE_TODO` intent, calling `crud.todos.update_todo` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Extends chatbot's capability to modify user's todos.
-   [ ] T020 [US3] Add logic for robust todo identification (by title, ID, etc.) when handling `UPDATE_TODO` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Ensures the correct todo is updated, especially with ambiguous natural language references.

---

### Phase 5: User Story 4 - Delete Todo (P2)

**Story Goal**: A user can successfully remove a todo item from their list using natural language.  
**Independent Test**: A user sends "Delete the buy milk todo", and the system confirms deletion, then the todo is no longer in their list.

**Tasks**:

-   [X] T021 [US4] Enhance `process_chat_message` to handle `DELETE_TODO` intent, calling `crud.todos.delete_todo` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Extends chatbot's capability to remove user's todos.
-   [X] T022 [US4] Add logic for robust todo identification (by title, ID, etc.) when handling `DELETE_TODO` (MODIFICATION to `backend/app/services/chat.py`)
    *   *Why this task exists*: Ensures the correct todo is deleted.

---

### Phase 6: Frontend Integration & Polish

**Story Goal**: Authenticated users can interact with the AI chatbot via a dedicated UI, sending messages and receiving responses.  
**Independent Test**: A logged-in user can access the chat UI, send a message, and receive a response, and the backend operations (e.g., todo creation) are visible.

**Tasks**:

-   [X] T023 [P] Create `frontend/src/app/chat/page.tsx` for the new chat UI (NEW FILE)
    *   *Why this task exists*: Provides the entry point for the chat interface.
-   [X] T024 [P] Create `frontend/src/components/ChatComponent.tsx` for chat message display and input (NEW FILE)
    *   *Why this task exists*: Implements the core interactive elements of the chat UI.
-   [X] T025 Integrate new chat API calls into `frontend/src/lib/api.ts` (MODIFICATION to `frontend/src/lib/api.ts`)
    *   *Why this task exists*: Enables the frontend to communicate with the new backend chatbot endpoint.
-   [X] T026 Implement authentication protection for the `/chat` route using existing Next.js middleware or `ProtectedRoute` (MODIFICATION to `frontend/middleware.ts` or `frontend/src/components/ProtectedRoute.tsx`)
    *   *Why this task exists*: Restricts access to the chat feature to authenticated users only.
-   [X] T027 Add navigation link to the Chat UI in an appropriate existing component (e.g., `frontend/src/components/Navbar.tsx`) (MODIFICATION to `frontend/src/components/Navbar.tsx`)
    *   *Why this task exists*: Makes the new chat feature discoverable by users.
-   [X] T028 Implement basic loading states and error handling in the Chat UI (MODIFICATION to `frontend/src/components/ChatComponent.tsx`)
    *   *Why this task exists*: Improves user experience during API calls and error scenarios.

