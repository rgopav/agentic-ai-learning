import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

secret = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash-lite",
  api_key = secret,
  temperature=0
)

template = ChatPromptTemplate.from_messages(
  [
    ("system","You are a US green energy infrastructure advisor. You only answer questions related to US EV or alternative hybrid fueling infrastructure. If a query is outside of this scope, politely decline to answer."),
    ("user","{input}")
  ]
)

guardrail_chain = template | llm

out_of_scope_query = {"input": "What is the capital of France?"}
response1 = guardrail_chain.invoke(out_of_scope_query)

in_scope_query = {"input": "Which state has highest density of EV charging stations? Respond in one sentece."}
response2 = guardrail_chain.invoke(in_scope_query)

print("--" * 40)
print("\n")
print(response1.content)
print("\n")
print('-' * 80)
print("\n")
print(response2.content)
print("\n")
print('-' * 80)