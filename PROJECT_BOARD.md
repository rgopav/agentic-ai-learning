# Agentic AI — Phase 1 Project Assignments
> **Goal:** Build independently from scratch. Close all reference code before you start. Note every gap in your "gotchas" doc.

---

## Project 01 — Employee Handbook RAG App

### Overview
Build a question-answering chatbot that answers employee queries using a company handbook PDF. This is the canonical RAG project and the foundation for everything that follows. Every concept you implement here — chunking, embedding, retrieval, chat history — reappears in more complex forms in later projects.

### Learning Objectives
- Understand the full RAG pipeline end-to-end
- Load and chunk a PDF document programmatically
- Generate and store vector embeddings in ChromaDB
- Wire a retrieval chain using LangChain
- Build a conversational Streamlit UI with persistent chat history

### Tech Stack
- **LangChain** — document loaders, text splitters, retrieval chain
- **ChromaDB** — local vector store
- **HuggingFace Transformers / OpenAI** — embedding model
- **Streamlit** — chat UI
- **PyPDF2 or pdfplumber** — PDF parsing

### Tasks

**Task 1 — Document Ingestion**
- Download or create a sample employee handbook PDF (10–20 pages is enough)
- Write a loader that reads the PDF and extracts raw text page by page
- Implement a chunking strategy using LangChain's `RecursiveCharacterTextSplitter`
- Experiment with `chunk_size` (try 500, 1000) and `chunk_overlap` (try 50, 200) — observe how this affects retrieval quality

**Task 2 — Embedding and Vector Store**
- Choose an embedding model (start with `all-MiniLM-L6-v2` from HuggingFace for free local use)
- Embed all chunks and persist them in a ChromaDB collection
- Write a helper function that checks if the collection already exists so you don't re-embed on every restart
- Test retrieval manually: write a function that takes a query string and returns the top-k most relevant chunks

**Task 3 — Retrieval Chain**
- Build a LangChain `RetrievalQA` or `ConversationalRetrievalChain`
- Connect your ChromaDB retriever to the chain
- Pass retrieved context into a prompt template that instructs the LLM to answer only from the provided context
- Handle the case where no relevant context is found — the LLM should say so rather than hallucinate

**Task 4 — Streamlit UI**
- Create a Streamlit app with a chat interface (`st.chat_input`, `st.chat_message`)
- Store conversation history in `st.session_state`
- Display sources (chunk text + page number) below each answer as an expandable section
- Add a sidebar showing: which document is loaded, number of chunks, embedding model name

**Task 5 — Evaluation (Basic)**
- Write 10 question-answer pairs manually from your handbook
- Run all 10 through your chatbot and record: correct / partially correct / wrong
- Note which question types fail (e.g. questions requiring multi-chunk reasoning)

### Acceptance Criteria
- [ ] App starts cleanly and loads the vector store without re-embedding
- [ ] Chat UI maintains history across turns in the same session
- [ ] Answers cite the source chunk they came from
- [ ] App gracefully handles questions not covered by the handbook
- [ ] You can explain every line of code without referring to documentation

### Stretch Goals
- Swap ChromaDB for FAISS and compare retrieval speed
- Add a re-ranker step after retrieval (cross-encoder scoring)
- Support uploading any PDF at runtime via `st.file_uploader`
- Add a "clear conversation" button that resets session state

### Interview Talking Points
Be ready to answer: *"Walk me through how you would build a RAG system."* After this project, your answer should cover: document loading → chunking strategy and why it matters → embedding model choice → vector store options → retrieval → prompt construction → response generation. Know the tradeoffs at each step.

---

## Project 02 — Personal Finance Advisor Agent

### Overview
Build an agent that reads a CSV file of bank transactions, uses Pandas to analyse the data, and answers natural language questions about spending. This project teaches you how agents use tools — functions the LLM can call — rather than retrieving from a vector store.

### Learning Objectives
- Understand the difference between RAG and tool-using agents
- Build custom tools and register them with an Agno agent
- Use Pandas and NumPy inside agent tools
- Practice structured output from LLMs (JSON responses)
- Handle agent memory within a session

### Tech Stack
- **Agno** — agent framework and tool registration
- **Pandas / NumPy** — data analysis inside tools
- **OpenAI / Anthropic Claude** — LLM backend
- **Streamlit** — upload UI and chat interface

### Tasks

**Task 1 — Data Setup**
- Create or download a realistic CSV of transactions with columns: `date`, `description`, `amount`, `category`
- Write a Pandas loading function that parses dates correctly and handles missing values
- Write at least 5 analytical functions (these will become your tools):
  - `get_total_by_category(category, month)` — total spend for a category in a given month
  - `get_top_merchants(n)` — top N merchants by total spend
  - `get_monthly_summary()` — income vs. expenses by month
  - `flag_unusual_transactions(threshold)` — transactions above a threshold
  - `calculate_savings_rate(month)` — income minus expenses as a percentage

**Task 2 — Tool Registration with Agno**
- Register each analytical function as an Agno tool with proper docstrings (the LLM reads these to decide which tool to call)
- Write clear, specific tool descriptions — vague descriptions cause the agent to pick the wrong tool
- Test each tool independently before wiring the agent

**Task 3 — Agent Construction**
- Create an Agno agent with a role definition: *"You are a personal finance advisor..."*
- Attach all tools to the agent
- Set context window rules: what the agent should and should not do (e.g. it should not give investment advice)
- Add a simple timeout so the agent doesn't loop indefinitely

**Task 4 — Structured Output**
- For the monthly summary query, instruct the agent to return a JSON object with fixed fields rather than free text
- Parse the JSON response and render it as a formatted table in Streamlit
- Handle the case where the LLM returns malformed JSON — add a retry or fallback

**Task 5 — Streamlit UI**
- File uploader for the CSV
- Chat interface for asking questions
- A pre-loaded "quick questions" panel with 5 common queries as buttons
- Session memory: the agent should remember earlier context (e.g. if you said "focus on June" earlier, it should remember)

### Acceptance Criteria
- [ ] Agent correctly selects the right tool for each type of question
- [ ] Structured output is reliably parsed into a table
- [ ] Agent handles ambiguous queries by asking a clarifying question (not just erroring)
- [ ] Session memory works across at least 5 turns
- [ ] You can explain what a tool docstring does and why it matters for LLM tool selection

### Stretch Goals
- Add a forecasting tool that uses NumPy to project next month's spending based on trends
- Let the agent generate a matplotlib bar chart and display it in Streamlit
- Add a second agent that acts as a "budget coach" and reviews the first agent's analysis

### Interview Talking Points
Be ready to explain: *"What is the difference between RAG and a tool-using agent? When would you use each?"* This project gives you a concrete answer. Also be ready to explain why tool docstrings matter — it's a common interview question about prompt engineering for agents.

---

## Project 03 — News Summariser Agent (ReAct)

### Overview
Build a ReAct (Reasoning + Acting) agent that takes a topic from the user, searches the web for recent articles, retrieves their content, and produces a structured news summary. This project teaches the ReAct loop — the most fundamental agentic pattern — and forces you to handle real-world messiness: bad URLs, paywalls, irrelevant results.

### Learning Objectives
- Understand the ReAct pattern: Thought → Action → Observation → Thought...
- Implement a multi-step agent that decides its own action sequence
- Handle tool errors gracefully without crashing the agent loop
- Practice logging and tracing agent reasoning steps
- Build a polished Streamlit UI showing the agent's "thinking" in real time

### Tech Stack
- **Agno** — ReAct agent with tool loop
- **SerpAPI or Tavily** — web search tool
- **BeautifulSoup / requests** — article content scraping
- **LangChain** — optional for summarisation chain
- **Streamlit** — UI with live reasoning trace

### Tasks

**Task 1 — Search Tool**
- Register a web search tool using SerpAPI (free tier) or Tavily
- The tool should accept a query string and return a list of `{title, url, snippet}` objects
- Add input validation: reject empty queries, truncate very long queries

**Task 2 — Article Retrieval Tool**
- Write a tool that takes a URL and returns the article's main text (strip navigation, ads, footers)
- Handle common failures: timeout, 403 forbidden, paywall (return a graceful message, not an exception)
- Limit extracted text to 2000 characters to avoid flooding the context window

**Task 3 — ReAct Agent**
- Build an Agno agent configured in ReAct mode
- Give it a system prompt that instructs it to: search first, retrieve the top 3 articles, then synthesise
- Implement a maximum step limit (e.g. 8 steps) so it cannot loop forever
- Log every Thought / Action / Observation to a list you can display in the UI

**Task 4 — Structured Summary Output**
- Instruct the agent to produce its final answer in a fixed structure:
  - **Headline** (1 sentence)
  - **Key Points** (3–5 bullet points)
  - **Sources** (list of URLs used)
  - **Sentiment** (positive / negative / neutral)
- Enforce this structure via your prompt template, not just a request

**Task 5 — Streamlit UI with Reasoning Trace**
- Text input for the user's topic
- While the agent runs, display each step in an expandable "Agent Reasoning" panel
- Show the final structured summary cleanly once the agent finishes
- Add a "retry" button that re-runs the agent with a rephrased query if the user isn't satisfied

### Acceptance Criteria
- [ ] Agent reliably completes within the step limit without crashing
- [ ] At least 2 different tools are called in a typical run
- [ ] Reasoning trace is visible and makes logical sense
- [ ] Article scraping handles at least 3 different failure modes gracefully
- [ ] Structured output format is consistent across runs

### Stretch Goals
- Add a "fact-check" tool that cross-references a claim from one article against another
- Implement a simple confidence score: how many sources agree on the main claim
- Add topic memory: the agent remembers past topics in a session and avoids repeating the same summary

### Interview Talking Points
Be ready to explain: *"What is ReAct and why is it useful?"* Your answer: ReAct interleaves reasoning traces with action calls, making the agent's decision process transparent and debuggable — critical for production systems. Also discuss: what happens if the agent loops? How do you prevent it?

---

## Project 04 — Resume Screener with HITL

### Overview
Build an agent that screens job applicants. The user uploads a job description and multiple resumes (PDFs). The agent scores each candidate, explains its reasoning, and presents a ranked shortlist — but waits for human approval before marking any candidate as "rejected". This is your first project with a formal Human-in-the-Loop (HITL) pattern.

### Learning Objectives
- Load and process multiple PDFs in a single pipeline
- Design a scoring rubric prompt and get consistent structured output
- Implement the HITL approval pattern (agent pauses, awaits human decision)
- Understand why HITL matters in high-stakes decisions
- Practice multi-document context management

### Tech Stack
- **LangChain** — document loaders, multi-document chain
- **Agno or LangGraph** — agent with pause/resume capability
- **ChromaDB** — optional, for semantic search across resumes
- **Streamlit** — upload UI, scoring display, approval buttons
- **pdfplumber** — robust PDF text extraction

### Tasks

**Task 1 — Document Ingestion**
- Write a batch PDF loader that accepts multiple uploaded files
- Extract text from each resume and the JD
- Store each resume as a structured object: `{filename, raw_text, candidate_name (extracted), pages}`
- Handle poor-quality PDFs (scanned, image-only) — detect and warn the user rather than silently failing

**Task 2 — Scoring Prompt Design**
- Design a prompt that instructs the LLM to score a candidate on 5 dimensions drawn from the JD:
  - Skills match (0–10)
  - Experience relevance (0–10)
  - Education fit (0–10)
  - Leadership signals (0–10)
  - Red flags (-5 to 0)
- Include chain-of-thought: the LLM must explain each score before giving the number
- Return output as a JSON object — validate it against a schema

**Task 3 — Batch Scoring Pipeline**
- Run the scoring prompt against every resume
- Display a live progress indicator in Streamlit as each resume is scored
- Catch and handle LLM errors (rate limits, malformed JSON) per-resume without stopping the whole batch

**Task 4 — HITL Approval Flow**
- After scoring, display the ranked shortlist with scores and reasoning
- For any candidate below a configurable threshold (e.g. total score < 25), show an "Approve Rejection" button
- The agent must not finalise a rejection until the human clicks approve
- Log every human decision with a timestamp to a session state audit trail
- Add an "Override" button: the human can promote a low-scoring candidate with a mandatory reason field

**Task 5 — Summary Report**
- Generate a one-page summary: total applicants, shortlisted, rejected (approved by human), pending
- For the top 3 candidates, produce a comparative paragraph explaining how they differ
- Allow the user to download the summary as a text file

### Acceptance Criteria
- [ ] All resumes are scored consistently using the same rubric
- [ ] No candidate is rejected without explicit human approval click
- [ ] Audit log captures every human decision
- [ ] System handles at least 10 resumes in a single session without errors
- [ ] You can explain why HITL is architecturally important, not just how to implement it

### Stretch Goals
- Add semantic search: "find all candidates with RAG experience" queries across the resume collection
- Add a "challenge" mode: hide scores from the human reviewer until after they rank candidates, then compare with AI scores
- Persist approved decisions to a SQLite database so they survive a page refresh

### Interview Talking Points
Be ready to discuss: *"Where in an agentic pipeline would you insert a human-in-the-loop checkpoint, and how do you implement it?"* This project gives you a concrete answer. Also discuss: what are the risks of removing HITL from this specific use case?

---

## Project 05 — Text-to-Image Prompt Studio

### Overview
Build a creative tool where users describe a scene in plain English, the LLM rewrites it as a highly optimised Stable Diffusion prompt, and the app calls an image generation API to produce the image. This project covers image generation concepts from your curriculum and teaches prompt engineering for a different modality.

### Learning Objectives
- Understand how diffusion models differ from LLMs
- Learn the structure of an effective Stable Diffusion prompt (subject, style, lighting, quality tags, negative prompts)
- Use the Transformers library for an optional local pipeline
- Practice API integration with an external image service
- Build an interactive before/after comparison UI

### Tech Stack
- **OpenAI (DALL-E 3) or Stability AI API** — image generation
- **HuggingFace Transformers** — optional local Stable Diffusion via `diffusers`
- **LangChain or direct API** — prompt rewriting LLM
- **Streamlit** — UI with image display and comparison
- **Pillow** — image handling

### Tasks

**Task 1 — Prompt Rewriting Chain**
- Write a LangChain chain (or direct LLM call) that takes a plain English description and rewrites it as an optimised image generation prompt
- Your rewriting prompt should instruct the LLM to add: art style, lighting conditions, camera angle, quality modifiers (`8k, photorealistic, detailed`), and negative prompt terms
- Test with at least 10 different input descriptions and review the rewritten prompts manually
- Add a "style preset" selector (photorealistic, anime, oil painting, watercolour) that appends style-specific tokens to the rewritten prompt

**Task 2 — Image Generation API**
- Integrate with DALL-E 3 via OpenAI's API (simplest) or Stability AI's REST API (closer to Stable Diffusion)
- Write a wrapper function that accepts the rewritten prompt and returns a PIL Image object
- Handle API errors: rate limits, content policy rejections, timeouts — show user-friendly messages

**Task 3 — Local Diffusion Pipeline (Stretch baseline)**
- Using HuggingFace `diffusers`, load a small Stable Diffusion model locally (e.g. `runwayml/stable-diffusion-v1-5`)
- Run inference on CPU (slow but educational) — understand what `num_inference_steps` and `guidance_scale` do
- Compare the output quality between local and API-based generation

**Task 4 — Prompt Iteration UI**
- Show the original user description and the rewritten prompt side by side
- Allow the user to manually edit the rewritten prompt before generating
- Generate the image and display it with the full prompt used underneath
- Add a prompt history panel showing the last 5 generated images with their prompts

**Task 5 — Negative Prompt Engineering**
- Add a "negative prompt" input field pre-populated with common quality-improving negatives (`blurry, deformed, watermark, low quality...`)
- Let the LLM suggest additional negative prompts based on the subject matter (e.g. for portraits: `extra fingers, distorted face`)
- Show a before/after toggle: same prompt with and without negative prompts

### Acceptance Criteria
- [ ] Rewritten prompts are consistently longer and more detailed than the original input
- [ ] Images are generated and displayed within the UI
- [ ] API errors are handled and shown as friendly messages, not stack traces
- [ ] Prompt history persists for the session duration
- [ ] You can explain how a diffusion model generates an image at a conceptual level (noise → denoise loop)

### Stretch Goals
- Add prompt versioning: save favourite prompts with user-defined labels
- Implement image variation: send a generated image back to the API to create variations
- Build a "prompt analyser" that scores a given prompt on likely quality dimensions

### Interview Talking Points
Be ready to explain: *"How does image generation with diffusion models differ from text generation with LLMs?"* Key points: diffusion models start with Gaussian noise and iteratively denoise guided by a text embedding, whereas LLMs autoregressively predict the next token. Know what `guidance_scale` controls (adherence to the prompt vs. image quality/diversity).

---

## Phase 1 Completion Checklist

Before moving to Phase 2, you should be able to:

- [ ] Build a RAG pipeline from scratch without referencing existing code
- [ ] Register and test custom tools in Agno
- [ ] Implement a ReAct agent loop with a step limit and error handling
- [ ] Explain the HITL pattern and name 3 real-world use cases for it
- [ ] Describe the difference between a diffusion model and an LLM
- [ ] Explain chunking strategies and their tradeoffs
- [ ] Write and validate structured JSON output from an LLM
- [ ] Build a Streamlit app with session state, file upload, and chat history

**Time estimate:** 3–4 weeks at ~10 hours/week, spending roughly 1 week per project.

---

*Next: Phase 2 — Memory, Graphs & Agentic RAG (Projects 06–10)*