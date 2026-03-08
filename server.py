from fastapi import FastAPI
from pydantic import BaseModel
from agent import process_chat

app = FastAPI(title = "Personal Travel Assistant")
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Server is running", "agent" : "Ready"}

@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
    ai_response = process_chat(request.message)
    return ai_response