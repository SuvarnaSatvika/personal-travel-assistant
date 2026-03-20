from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import process_chat
from pdf_generator import generate_itinerary_pdf
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # This allows any website to talk to your API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ItineraryRequest(BaseModel):
    destination: str
    events: list = []
    itinerary: list = []

@app.get("/")
def home():
    return {"status": "Server is running", "agent" : "Ready"}

@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
    ai_response = process_chat(request.message)
    return ai_response

@app.post("/api/generate-pdf")
async def generate_pdf(data: dict):
    print(f"DEBUG FROM FRONTEND: {data}")
    file_path = generate_itinerary_pdf(data)
    return FileResponse(file_path)
