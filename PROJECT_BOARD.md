# CineAgent AI - MVP Implementation Board

## Phase 1: Core Python & Data Engine
**Goal:** Build the foundation to ingest, clean, and store regional movie metadata using Advanced Python OOP and relational databases.

### [ ] CA-1.1: Repo Setup & OOP Base Class Architecture
* **Description:** Initialize the repository, set up virtual environments (`venv` or `poetry`), and create abstract base classes that future agents and data managers will inherit from.
* **Curriculum Covered:** Module 11 (Object-Oriented design for multi-agent systems).
* **Architecture & Files:**
    * `requirements.txt` / `pyproject.toml`
    * `src/core/base.py`: Create `class BaseAgent(ABC)` and `class BaseTool(ABC)`.
    * `src/config/settings.py`: Create `class AppSettings` to load environment variables.

### [ ] CA-1.2: Relational Database Architecture (SQLite)
* **Description:** Set up a local SQLite database using SQLAlchemy to store structured movie metadata and streaming availability, acting as the ground-truth "Relational Brain".
* **Curriculum Covered:** Module 11 (Advanced Python for AI).
* **Architecture & Files:**
    * `src/db/database.py`: Functions `get_db_session()`, `init_db()`.
    * `src/db/models.py`: Create SQLAlchemy classes: `class Movie(Base)`, `class StreamingAvailability(Base)`.

### [ ] CA-1.3: Data Pipeline (Pandas/NumPy) & Web Scraper
* **Description:** Build a pipeline to ingest raw regional movie data (e.g., CSVs or mocked API responses), clean it using Pandas, and normalize multilingual text for embedding.
* **Curriculum Covered:** Module 11 (Data manipulation with Pandas/NumPy), Module 10 (Handling multilingual and regional data).
* **Architecture & Files:**
    * `src/data/ingestion.py`: Create `class DataProcessor`.
    * `src/data/scraper.py`: Functions `fetch_regional_metadata()`, `clean_text_numpy_vectorization()`.

---

## Phase 2: Middleware & Local RAG
**Goal:** Implement the "Semantic Brain" by running LLMs entirely locally, chunking the movie plots, and storing them in a vector database for semantic search.

### [ ] CA-2.1: Local Model Setup (Ollama/Gemma)
* **Description:** Configure Ollama to run locally. Integrate the Python application with the local Gemma model for text generation and a local sentence-transformer for embeddings.
* **Curriculum Covered:** Module 8 (Running Gemma locally, Ollama setup, Hardware optimization).
* **Architecture & Files:**
    * `src/llm/local_runner.py`: Create `class OllamaManager` with functions `generate_text()`, `check_hardware_status()`.

### [ ] CA-2.2: Vector Store Integration (FAISS/Chroma)
* **Description:** Process the cleaned movie data, generate text embeddings, and store them in a local vector database.
* **Curriculum Covered:** Module 2 (RAG Concepts), Module 10 (Structuring regional movie databases).
* **Architecture & Files:**
    * `src/rag/vector_store.py`: Create `class ChromaDBManager` or `class FAISSRetriever`.
    * Functions: `add_documents()`, `similarity_search()`.

### [ ] CA-2.3: Base Retrieval Logic & Query Routing
* **Description:** Build the logic that decides if a user's query needs to hit the Vector Store (for plots) or the SQLite DB (for exact IDs/URLs).
* **Curriculum Covered:** Module 2 (LangChain, Llama Index basics).
* **Architecture & Files:**
    * `src/rag/router.py`: Create `class QueryRouter`.
    * Functions: `route_query()`, `format_context()`.

---

## Phase 3: Multi-Agent Orchestration (The Brains)
**Goal:** Deploy autonomous agents that collaborate to search for movies, verify streaming links, and compile the final response.

### [ ] CA-3.1: Agno Single-Agent Setup for OTT Lookup
* **Description:** Build a blazing-fast, single-purpose agent using Agno to mock/ping OTT APIs (Aha, Prime, SonyLIV) for active streaming links.
* **Curriculum Covered:** Module 5 (Agno Fundamentals: Build first single agent, tool calls, timeouts, light logging).
* **Architecture & Files:**
    * `src/agents/agno_broker.py`: Create `class OTTLookupAgent`.
    * Functions: `configure_agno_agent()`, `execute_search_tool()`.

### [ ] CA-3.2: CrewAI Multi-Agent Team Orchestration
* **Description:** Define a Crew with two personas: A Curator (searches RAG for the movie) and an Analyst (uses Agno tools to find the stream).
* **Curriculum Covered:** Module 4 (Defining Agents with roles/goals, Tool routing, Crew Orchestration, Collaborative workflows).
* **Architecture & Files:**
    * `src/agents/crew_manager.py`: Create `class MovieResearchCrew`.
    * Functions: `create_curator_agent()`, `create_analyst_agent()`, `define_tasks()`, `kickoff_crew()`.

### [ ] CA-3.3: LangGraph Stateful Orchestration
* **Description:** Wrap the RAG and CrewAI logic inside a LangGraph state machine to handle conditional routing, memory, and automated retries if agents fail.
* **Curriculum Covered:** Module 4 (Failure handling: retries, fallbacks), Module 3 (Agentic AI Architecture).
* **Architecture & Files:**
    * `src/graph/workflow.py`: Create `class MovieGraph`.
    * Functions: `build_graph()`, `node_retrieve_data()`, `node_execute_crew()`, `compile_graph()`.

---

## Phase 4: UI & Human-In-The-Loop (HITL)
**Goal:** Build the interactive frontend using Streamlit to visualize agent thoughts and require human approval before saving new data.

### [ ] CA-4.1: Streamlit Chat Interface & Agent Visualization
* **Description:** Create a dark-mode Streamlit UI. Implement chat history and visualize the agent's thought process (tool calling) in real-time.
* **Curriculum Covered:** Module 6 (Simple UI Gradio/Streamlit), Module 7 (Observability and Monitoring topics).
* **Architecture & Files:**
    * `app.py`: Main entry point.
    * `src/ui/components.py`: Functions `render_sidebar()`, `render_movie_cards()`, `stream_agent_thoughts()`.

### [ ] CA-4.2: Human-In-The-Loop (HITL) Integration
* **Description:** Add a pause state in LangGraph that pushes a notification to the UI, requiring the user to click "Approve" before a discovered streaming link is committed to the SQLite DB.
* **Curriculum Covered:** Module 6 (Human-in-the-loop review actions).
* **Architecture & Files:**
    * `src/graph/workflow.py` (Update): Add `interrupt_before=["save_to_db"]`.
    * `src/ui/hitl_dashboard.py`: Functions `render_pending_approvals()`, `handle_approval_click()`.

---

## Phase 5: AI Quality Assurance & Testing
**Goal:** Prove the system is robust by applying AI-specific testing and traditional software QA principles.

### [ ] CA-5.1: RAG Pipeline Evals & Hallucination Checks
* **Description:** Write validation checks to ensure the LLM does not hallucinate streaming links or movie plots, measuring context relevance.
* **Curriculum Covered:** Module 9 (Evaluating RAG pipelines, Hallucination mitigation).
* **Architecture & Files:**
    * `tests/test_rag_evals.py`: Create `class TestRAGFaithfulness`.
    * Functions: `evaluate_context_precision()`, `check_hallucination()`.

### [ ] CA-5.2: Automated Agent State Testing
* **Description:** Use PyTest to mock tool calls and verify that LangGraph states transition correctly and CrewAI outputs conform to the expected JSON schema.
* **Curriculum Covered:** Module 9 (Transitioning from traditional QA to AI testing, Automated testing for Agentic systems).
* **Architecture & Files:**
    * `tests/test_agents.py`: Create `class TestCrewOrchestration`.
    * Functions: `test_agent_schema_output()`, `test_langgraph_routing()`.