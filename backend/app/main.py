from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import auth_router
from app.api.v1.tasks import tasks_router
from app.routers import chat

app = FastAPI()

# ✅ CORS (MANDATORY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Auth router (/api/signup, /api/login)
app.include_router(auth_router, prefix="/api", tags=["auth"])

# 2. Tasks router (/api/{user_id}/tasks)
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

# 3. Chat router (/api/v1/chat/send-message)
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
def health():
    return {"status": "ok"}