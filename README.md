# AI Travel Assistant

A full-stack, AI-powered travel planning application that acts as a personal concierge. Users can chat naturally with the AI to generate highly customized, multi-day travel itineraries, fetch live local events, and export their finalized plans as a formatted PDF.

### [View Live Demo](https://personal-travel-assistant-agrw.vercel.app/)

---

## Key Features
* **Conversational AI Interface:** Built with LangChain and Google Gemini, capable of maintaining context and understanding complex user preferences.
* **Live Event Integration:** Dynamically fetches real-world, localized events and concerts using the Ticketmaster API.
* **Real-Time Web Search:** Utilizes DuckDuckGo Search (`ddgs`) to ground the AI's recommendations in current, real-world data.
* **Smart Tool-Calling:** The AI autonomously decides when to trigger backend Python functions to fetch data or compile the final itinerary.
* **Instant PDF Generation:** Converts the finalized JSON itinerary data into a cleanly formatted, downloadable PDF document.
* **Resilient Architecture:** Includes graceful error handling for API rate limits and quota restrictions to ensure a smooth, crash-free user experience.

---

## Tech Stack

### Frontend (Client)
* **Framework:** React.js (via Vite)
* **Styling:** Tailwind CSS
* **Deployment:** Vercel

### Backend (Server)
* **Framework:** Python & FastAPI
* **AI Orchestration:** LangChain & Google Generative AI (Gemini)
* **PDF Compilation:** FPDF
* **Deployment:** Render

---

## Architecture
This project utilizes a decoupled architecture, separating the client interface from the heavy AI computation. The React frontend sends user prompts to the FastAPI backend, which processes the text, orchestrates external API calls (Gemini, Ticketmaster, DDG), and streams the formatted response or tool outputs back to the UI.

---

## Local Development Setup

To run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/SuvarnaSatvika/personal-travel-assistant.git
cd ai-travel-assistant
```

### 2. Backend Setup (Python)
Ensure you have Python 3.9 or higher installed.
```bash
# Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Environment Variables**
Create a `.env` file in the root directory and add your secret API keys:
```env
GOOGLE_API_KEY=your_gemini_key_here
TICKETMASTER_API_KEY=your_ticketmaster_key_here
```

**Start the API Server**
```bash
uvicorn server:app --reload
```
*The backend will run on `http://127.0.0.1:8000`*

### 3. Frontend Setup (React/Vite)
Open a new terminal window/tab in the project root.
```bash
# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
Navigate to `http://localhost:5173` in your browser to interact with the AI.

---

## Deployment
* **Frontend:** Configured for zero-config deployment on Vercel (Framework Preset: Vite).
* **Backend:** Configured for deployment on Render. Ensure `WEB_CONCURRENCY` is managed and CORS middleware in `server.py` is configured to accept requests from your deployed frontend domain.
