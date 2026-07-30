# Research Findings: Phase III Todo AI Chatbot

**Feature Branch**: `001-todo-ai-chatbot`  
**Date**: 2026-06-30  
**Related Plan**: [specs/001-todo-ai-chatbot/plan.md](specs/001-todo-ai-chatbot/plan.md)

## Resolved Unknowns from Technical Context

### 1. LLM Provider Integration Strategy

*   **Decision**: Integrate with Google Gemini API using the official Google Generative AI Python SDK (`google-generativeai`). The integration will be abstracted behind a common interface within `backend/app/services/ai/`.
*   **Rationale**:
    *   The Google Generative AI SDK provides a high-level, idiomatic Python interface for interacting with Gemini models, simplifying API calls, token management, and error handling.
    *   Abstracting the LLM interaction ensures that the core business logic remains decoupled from the specific AI provider, allowing for future changes to Claude or other models with minimal code modification.
    *   Leverages the existing tooling and familiarity within the Gemini CLI context.
*   **Alternatives Considered**:
    *   Direct HTTP calls to the Gemini API: Rejected due to increased complexity in handling authentication, request/response serialization, and error parsing compared to using a dedicated SDK.
    *   Integrating with Anthropic Claude directly: Rejected for initial implementation to maintain focus and simplify initial setup; abstraction allows for future addition.

### 2. Structured JSON Output Format from LLM

*   **Decision**: The LLM will be prompted to output a JSON object adhering to a predefined schema that includes `intent` (e.g., "CREATE_TODO", "LIST_TODOS", "UPDATE_TODO", "DELETE_TODO", "UNKNOWN") and `entities` (a dictionary of extracted parameters like `title`, `due_date`, `status`, `target_id`).
    *   **Example JSON for CREATE_TODO**: `{"intent": "CREATE_TODO", "entities": {"title": "Buy milk", "due_date": "2026-07-01"}}`
    *   **Example JSON for LIST_TODOS**: `{"intent": "LIST_TODOS", "entities": {"filter_status": "pending"}}`
    *   **Example JSON for UNKNOWN**: `{"intent": "UNKNOWN", "entities": {}}`
*   **Rationale**:
    *   Structured JSON output provides a clear, machine-readable contract between the LLM and the backend application logic, enabling reliable parsing and deterministic actions.
    *   Allows for flexible extraction of various entities required for different todo operations.
*   **Alternatives Considered**:
    *   Natural language output requiring further parsing: Rejected due to increased complexity, potential for ambiguity, and higher maintenance burden for extracting structured data.
    *   Multiple LLM calls for intent and entities separately: Rejected for initial design to reduce latency and token usage, favoring a single, comprehensive JSON output.

### 3. Abstracting LLM Interaction for Extensibility

*   **Decision**: Implement a `LLMService` abstract base class (or interface) in `backend/app/services/ai/base.py`. Concrete implementations (e.g., `GeminiLLMService` in `backend/app/services/ai/gemini.py`) will inherit from this base class. The `chat` router will depend on this abstract service.
*   **Rationale**: This Strategy pattern promotes loose coupling, allowing different LLM providers to be integrated or swapped out without modifying the core API logic or business rules. It enhances maintainability and future-proofing.
*   **Alternatives Considered**:
    *   Directly calling LLM SDK functions in the router/service layer: Rejected as it tightly couples the application to a specific LLM provider, making future changes difficult.
    *   Using a generic HTTP client with different configuration for each LLM: Rejected as it re-implements SDK functionality and introduces unnecessary complexity.

### 4. LLM Prompt Engineering

*   **Decision**: Develop a system-level prompt that clearly defines the LLM's role, the expected JSON output format, the available intents, and instructions for entity extraction.
    *   The prompt will include examples of user inputs and their corresponding desired JSON outputs (few-shot learning).
    *   The prompt will instruct the LLM to default to an "UNKNOWN" intent if it cannot confidently classify the user's request.
    *   The prompt will emphasize extracting entities even if the intent is "UNKNOWN" if they seem relevant.
*   **Rationale**:
    *   Effective prompt engineering is crucial for guiding the LLM to produce consistent, accurate, and structured responses.
    *   Few-shot examples significantly improve LLM performance for specific tasks like intent classification and entity extraction.
    *   Explicit instructions for unknown intents ensure graceful handling of unparseable requests.
*   **Alternatives Considered**:
    *   Minimal prompting (relying on LLM's general knowledge): Rejected due to high risk of inconsistent or incorrect output for domain-specific tasks.
    *   Complex fine-tuning of LLM: Rejected for initial implementation due to time constraints and the effectiveness of prompt engineering for this scope. Fine-tuning could be a future optimization.