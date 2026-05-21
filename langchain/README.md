# Showcase-Ready LangChain Portfolio Exercises 💼🚀

This directory contains a complete, hands-on learning curriculum built using **LangChain (modern v0.2/v0.3 syntax)** and integrated with **Google Gemini** models. 

Each file is a **Jupyter Notebook (.ipynb) exercise template** designed around high-value, real-world business cases. Each notebook contains professional coding challenges, architecture scaffolding, hints, and a **💼 Portfolio Showcase Tip** to help you present these projects to potential employers on GitHub.

---

## 📂 Portfolio Curriculum Roadmap

| Exercise File | Business Scenario | Key LangChain Concepts | Recruitment Highlights |
| :--- | :--- | :--- | :--- |
| 🟢 [**`01_simple_llm_exercise.ipynb`**](file:///c:/Users/revan/workspace/agentic-ai-learning/langchain/01_simple_llm_exercise.ipynb) | **Customer Support Triage Engine** | `ChatGoogleGenerativeAI`, messages, API invocation. | Demonstrates structured LLM classification without fragile regex or manual reviews. |
| 🟢 [**`02_prompt_templates_exercise.ipynb`**](file:///c:/Users/revan/workspace/agentic-ai-learning/langchain/02_prompt_templates_exercise.ipynb) | **Dynamic B2B Sales Outreach Generator** | `ChatPromptTemplate`, variable injection, role prompting. | Shows clean prompt engineering practices, separating system roles from human content. |
| 🟡 [**`03_lcel_chain_exercise.ipynb`**](file:///c:/Users/revan/workspace/agentic-ai-learning/langchain/03_lcel_chain_exercise.ipynb) | **Automated Content CMS Blog Generator** | LCEL pipeline (`|`), `StrOutputParser`, `.stream()`. | Showcases building responsive UI dashboards using advanced real-time token streaming. |
| 🔴 [**`04_rag_exercise.ipynb`**](file:///c:/Users/revan/workspace/agentic-ai-learning/langchain/04_rag_exercise.ipynb) | **Enterprise HR Policy Q&A System** | Text splitting, `GoogleGenerativeAIEmbeddings`, `FAISS`, RAG chain. | Highlights search-grounding and retrieval systems that eliminate LLM hallucinations. |
| 🔴 [**`05_agent_exercise.ipynb`**](file:///c:/Users/revan/workspace/agentic-ai-learning/langchain/05_agent_exercise.ipynb) | **Smart Financial Planner & Advisor** | Custom `@tool` decoration, `create_tool_calling_agent`, `AgentExecutor`. | Demonstrates state-of-the-art agent loops, delegating math to exact Python calculators. |

---

## 🛠️ Environment Setup & Prerequisites

To execute these notebooks, set up a Python environment with Jupyter support.

### 1. Install Required Packages
Run the following pip command in your terminal:
```bash
pip install langchain langchain-google-genai langchain-community faiss-cpu python-dotenv jupyter ipykernel
```

### 2. Configure Your API Key
1. Create a `.env` file from the template:
   ```bash
   cp .env.template .env
   ```
2. Open `.env` and fill in your Gemini API Key:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

---

## 🚀 How to Run the Exercises

### Option A: VS Code (Recommended)
1. Open this workspace folder in VS Code.
2. Install the **Jupyter** extension in VS Code.
3. Open any `.ipynb` file (e.g. `01_simple_llm_exercise.ipynb`).
4. Select your python interpreter/environment in the top-right kernel dropdown.
5. Code your solution under the `# TODO` comments and click **Run** (or `Ctrl+Enter`) on each cell to test your implementation!

### Option B: Jupyter Lab / Jupyter Notebook
1. Navigate to this directory in your terminal and run:
   ```bash
   jupyter notebook
   ```
2. Click on the target notebook file in your web browser interface.
3. Code and run your solutions in place!

---

## 🌟 Pro-Tips for Your GitHub Profile Showcase

When you are ready to upload this to GitHub for job applications, make sure to:
1. **Commit your completed notebooks**: Clear the output cells first, or run them successfully so recruiters can see the working execution logs.
2. **Expand the project**: Add a `Solutions/` folder if you want to showcase your final code, keeping the main templates clean.
3. **Enhance your main README**: Copy sections of this guide and include screenshots of your agent execution outputs to make your repo highly visual and interactive.
