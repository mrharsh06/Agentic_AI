from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import io
import sys
import re
import io
import sys
from fastapi.responses import JSONResponse

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_kEY")

app = FastAPI()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
        )
    ],
    instructions=["Use tables to Display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent = Agent(
    team=[web_search_agent, finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Always include sources", "Use tables to Display the data"],
    show_tools_calls=True,
    markdown=True,
)

# Function to remove ANSI escape sequences
def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    user_input = data.get("query", "")
    if not user_input:
        return JSONResponse({"error": "Query not provided"}, status_code=400)

    try:
        # Capture the output of print_response
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the agent's print_response method
        multi_ai_agent.print_response(user_input, stream=False)

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Retrieve and sanitize the output
        raw_response = captured_output.getvalue()
        sanitized_response = remove_ansi_escape_sequences(raw_response)

        return {"response": sanitized_response.strip()}
    except Exception as e:
        sys.stdout = sys.__stdout__  # Ensure stdout is reset on error
        return JSONResponse({"error": str(e)}, status_code=500)