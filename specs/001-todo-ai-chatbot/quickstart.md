# Quickstart Guide: Phase III Todo AI Chatbot Integration

**Feature Branch**: `001-todo-ai-chatbot`  
**Date**: 2026-06-30  
**Related Plan**: [specs/001-todo-ai-chatbot/plan.md](specs/001-todo-ai-chatbot/plan.md)
**Related Spec**: [specs/001-todo-ai-chatbot/spec.md](specs/001-todo-ai-chatbot/spec.md)

This guide provides the necessary steps to set up and run the Phase III Todo AI Chatbot feature. It assumes you have the existing Phase I and Phase II project setup and running.

## 1. Prerequisites

*   Existing project setup (FastAPI backend, Next.js frontend, PostgreSQL database).
*   Python 3.8+ and Node.js 18+ installed.
*   `pip` and `npm` (or `yarn`) package managers.
*   Access to a Google Gemini API Key.

## 2. Backend Setup

### 2.1. Environment Variables

Add the following to your `.env` file in the `backend/` directory:

```dotenv
# Google Gemini API Key for AI Chatbot integration
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual Gemini API Key.

### 2.2. Install New Python Dependencies

Navigate to the `backend/` directory and install the new Google Generative AI client library:

```bash
cd backend/
pip install -r requirements.txt
pip install google-generativeai # Ensure it's added to requirements.txt for future use
```

**Note**: You should add `google-generativeai` to `backend/requirements.txt` manually for project consistency.

### 2.3. Run Database Migrations

A new table for `ChatHistory` needs to be created. Ensure your Alembic environment is configured correctly.

```bash
cd backend/
alembic revision --autogenerate -m "Add chat_history table"
alembic upgrade head
```

Verify that the `chat_history` table is created in your PostgreSQL database.

### 2.4. Run the Backend

Start the FastAPI backend application:

```bash
cd backend/
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend should now be running and exposing the new `/api/v1/chat/send-message` endpoint.

## 3. Frontend Setup

### 3.1. Install New Node.js Dependencies

Navigate to the `frontend/` directory and install any new React/Next.js dependencies if required (e.g., for UI components).

```bash
cd frontend/
npm install # or yarn install
```

### 3.2. Update Backend API Endpoint

Ensure your frontend configuration points to the correct backend API. If running locally, this might already be set up, but verify `NEXT_PUBLIC_BACKEND_URL` in your frontend's `.env` or configuration.

```dotenv
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
```

### 3.3. Run the Frontend

Start the Next.js frontend application:

```bash
cd frontend/
npm run dev # or yarn dev
```

The frontend should now be running, and you can navigate to the new chat UI page (e.g., `/chat`) after logging in.

## 4. Testing the Chatbot

1.  Log in to the frontend application.
2.  Navigate to the new chat UI page (e.g., `/chat`).
3.  Type a natural language message related to your todos (e.g., "Add a todo to buy milk tomorrow", "Show my pending tasks", "Mark 'buy milk' as done").
4.  Observe the chatbot's response and verify that todo operations are reflected in your todo list.
