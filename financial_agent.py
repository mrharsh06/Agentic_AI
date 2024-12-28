from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key=os.getenv("OPENAI_API_kEY")


##This is my first Web Search Agent
web_search_agent=Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

#Financial Agent
Finance_agent=Agent(
    name="Fianance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True,stock_fundamentals=True,)],
    instructions=["Use tabls to Display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent=Agent(
    team=[web_search_agent ,Finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Always include sources","Use tabls to Display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("summarize anlayst recommendation and share the latest news for NVDA",stream=True)
