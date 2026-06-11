"""
Langchain, Google genai, basic agent. 
"""


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  api_key=GEMINI_API_KEY,
  temperature=0.3
)

chat_agent = create_agent(
  model=llm
) 

response = chat_agent.invoke(
  {
    "messages":
    [{
      "role":"user",
      "content": "How does software and AI companies use Discord?"

    }]
  }
)

print(response["messages"][-1].content)

