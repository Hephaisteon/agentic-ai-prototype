# agentic-ai-prototype

## Description
This project implements an agentic AI that answers software-specific questions by reasoning over different information sources and iteratively improving its answers. The agent follows a stateful workflow, orchestrates based on collected context, tackles hallucination by critique-based refinement and safe fallbacks and ensures termination.

It explores
- Semantic PDF search
- Web-based information retrieval
- Tool selection
- Similarity thresholds
- Confidence scoring
- Critique-based refinement
- Iteration control
- Tracing
- Multi-agent architecture


## Agent architecture:

The system consists of two agent: One research agent and one email agent
The research agent is implemented as a LangGraph-based agentic workflow where each node operates on a shared state and makes explicit routing decisions. The email agent is triggered if a user requests to get the results of the research agent to be sent via email.

<img width="487" height="677" alt="architecture" src="https://github.com/user-attachments/assets/20de7b4d-c3e5-4788-97db-0f88f53e7e08" />



## How to run
pip install -r requirements.txt
python main.py


## NOTE: 
- local_doc_search node
  
  This project supports optional local document retrieval using FAISS vectorstores built from PDF documentation.
  The vectorstores are not included in this repository to avoid redistributing third-party or proprietary materials.
  The agent is designed to also operate without local vectorstores:
  - If no vectorstores are present:
    - the local document search step is skipped automatically
    - the agent continues using web-based retrieval and fallback strategies
  
  Using Local Document Retrieval (Optional)
  
  To enable PDF-based retrieval:
  - Provide your own PDF sources (e.g. public documentation)
  - Update the paths in pdf_vector_storage.py
  - Run the indexing step once:
  
  python pdf_vector_storage.py
  
  After indexing, the agent will automatically incorporate local document context into its reasoning flow.

- safe_file node

  The agent includes a `save_file` node that saves the final answer,
  source references, and agent execution trace to a local text file. This allows to inspect the agent’s reasoning steps.
  The txt file will be stored in the project environment.

