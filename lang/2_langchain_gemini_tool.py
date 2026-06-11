"""
A program to get answer from Gemini using Tools.
"""

import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

import os
from dotenv import load_dotenv

load_dotenv()

SECRET=os.getenv("GEMINI_API_KEY")

def get_weather(city: str) -> str:
  """Get temperature of city"""
  return f"{city} is called City of rain. So it's mostly rainy here in {city}"

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  temperature=0,
  api_key=SECRET,
)

chat_agent= create_agent(
  llm,
  tools=[get_weather]
)

response = chat_agent.invoke(
  {
  "messages": [{
    "role": "user",
    "content": "What's the weather in Seattle?"
    }]
  }
)

print(response["messages"][-1].content)