import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

secret = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash-lite",
  api_key=secret,
  temperature=0
)

template = ChatPromptTemplate.from_messages(
  [
    ("system", "You are a US green energy infrastructure advisor. "
    "You only answer questions related to US EV infrastructure"),
    ("user", "{input}")
  ]
)

guardrail_chain = template | llm

out_of_scope_query={"input": "What is the capital of France?"}
response1 = guardrail_chain.invoke(out_of_scope_query)
print(response1.content)

in_scope_query={"input": "What is CCS port?"}
response2 = guardrail_chain.invoke(in_scope_query)
print(response2.content)

