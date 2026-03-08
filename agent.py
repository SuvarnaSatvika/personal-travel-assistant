import json
import os
import requests

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field

#Loading API key from .env file
load_dotenv(override=True)

# --- ADD THIS DEBUG BLOCK ---
current_key = os.getenv("GOOGLE_API_KEY")

class Activity(BaseModel):
    time: str = Field(description="Time of the day")
    description: str = Field(description="Description of the activity")
    location: str = Field(description="Where the activity takes place")

class DayPlan(BaseModel):
    day_number: int
    activities: list[Activity]

@tool
def export_to_ui(destination: str, total_budget: str, days: list[DayPlan]):
    """Call this tool ONLY when the user is happy with the itinerary and wants to finalize or save it"""

    final_data = {
        "destination": destination,
        "total_budget_estimate": total_budget,
        "days": [day.dict() for day in days]
    }
    return json.dumps(final_data, indent=2)

ddg_search = DuckDuckGoSearchRun()

@tool
def web_search(query: str):
    """Use this tool to find any real time data user asks for, like weather, status of the place"""
    try:
        result = ddg_search.invoke(query)
        return str(result[:1000])
    except Exception as e:
        return f"Search failed: {e}"

@tool
def get_local_events(location: str):
    """Use this tool to find live events, concerts and festivals.
     NEVER tell user to check a website or listing platform. Always provide the real events"""

    print(f"\nAccessing event database from TICKETMASTER for {location}")

    api_key = os.getenv("TICKETMASTER_API_KEY")
    if not api_key:
        return "Error: Ticket master API key not found"

    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
        "city": location,
        "apikey": api_key,
        "size": 5,
        "sort": "date,asc"
    }

    try:
        event_response = requests.get(url, params=params)
        event_response.raise_for_status()
        data = event_response.json()

        if "_embedded" not in data or "events" not in data["_embedded"]:
            return json.dumps({"message": f"No upcoming events found in {location}"})

        events_list = []
        for event in data["_embedded"]["events"]:
            name = event.get("name", "Unknown event")
            url = event.get("url", "")

            venue = "unknown venue"
            if "venues" in event.get("_embedded", {}):
                venue = event["_embedded"]["venues"][0].get("name", "unknown venue")

            date = event.get("dates", {}).get("start", {}).get("localDate", "unknown date")
            time = event.get("dates", {}).get("start", {}).get("localTime", "Time TBD")
            events_list.append({
                "name" : name,
                "date" : date,
                "time" : time,
                "venue" : venue,
                "booking_link" : url
            })
        return json.dumps(events_list)
    except Exception as e:
        return f"Failed to fetch events from ticket master: {str(e)}"


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0.2, google_api_key=current_key)
llm_with_tools = llm.bind_tools([export_to_ui, web_search, get_local_events])


system_prompt = """
You are the best travel agent. Your job is to create logical, well-structured
itineraries. 
You must strictly adhere to user's constraints, including:
1.Budget
2.Number of travellers
3.Food preferences
4.Preferred Transportation
If you are not clear on any of the real-time event data, don't 
generate imaginary information. If you don't know it, just say so or give an estimate
and label it as estimate.
If the user asks follow-up questions, use the context of the itinerary you already generated.
If the user asks for real-time data, use the web_search tool to find the exact answer.
If the user asks for live event, concerts or festivals, you MUST use the get_local_events tool.
NEVER tell the user to check a website or listing platform. You MUST provide the actual event names and venues directly to the user.
Do not call to 'export_to_ui' tool until the user explicitly agrees the plan is perfect and tells you to finalize or save it.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history")
])

chain = prompt | llm_with_tools

chat_history = []
print("Travel agent is ready! (Type 'finalize' when happy\n")

def process_chat(user_input: str):
    """Takes a user string, runs the loop and returns the response"""

    chat_history.append(HumanMessage(content=user_input))

    while True:
        response = chain.invoke({"chat_history": chat_history})

        if not response.tool_calls:
            agent_text = response.content if isinstance(response.content, str) else "".join([b.get("text", "") for b in response.content if "text" in b])

            if not agent_text.strip():
                agent_text = "I am sorry I could not process that! Can you rephrase?"

            chat_history.append(AIMessage(content=agent_text))
            return {"type": "chat", "content" : agent_text}

        chat_history.append(response)

        for tool_call in response.tool_calls:
            if tool_call['name'] == 'export_to_ui':
                return {"type": "json_ui", "content": tool_call['args']}

            elif tool_call['name'] == 'web_search':
                query = tool_call['args'].get('query', '')
                print(f"searching the web for {query}")

                search_result = web_search.invoke({"query": query})
                chat_history.append(ToolMessage(
                    tool_call_id = tool_call['id'],
                    content = str(search_result)
                ))

            elif tool_call['name'] == 'get_local_events':
                location = tool_call['args'].get('location')
                if not location:
                    return "Error: You must provide a location to get events"

                event_data = get_local_events.invoke({"location" : location})

                chat_history.append(ToolMessage(
                    tool_call_id = tool_call['id'],
                    content=str(event_data)
                ))
