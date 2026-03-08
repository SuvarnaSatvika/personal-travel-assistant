from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import process_chat
from pdf_generator import generate_itinerary_pdf
import os

app = FastAPI(title = "Personal Travel Assistant")
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
def create_pdf(request: ItineraryRequest):
    print("\n Generating PDF....")

    try:
        itinerary_data = request.model_dump() if hasattr(request, 'model_dump') else request.dict()

        file_path = generate_itinerary_pdf(itinerary_data)

        return FileResponse(
            path=file_path,
            filename="My Itinerary.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        return {"error" : f"Failed to generate PDF {str(e)}"}
