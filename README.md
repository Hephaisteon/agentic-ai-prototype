# agentic-ai-prototype

## Description

This project implements an agentic AI that answers software-specific questions by reasoning over different information sources and iteratively improving its answers. The agent follows a stateful workflow, orchestrates based on collected context, tackles hallucination by critique-based refinement and safe fallbacks, and ensures termination.

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

The system consists of two agents: 
- Research agent
  - The research agent is implemented as a LangGraph-based agentic workflow where each node operates on a shared state and makes explicit routing decisions.
- Email agent
  - The email agent is triggered if a user requests to get the results of the research agent to be sent via email.

Graph Visual:

<img width="487" height="677" alt="architecture" src="https://github.com/user-attachments/assets/20de7b4d-c3e5-4788-97db-0f88f53e7e08" />




## Motivation & Real-World Context

In large organizations, users often face challenges of identifying up-to-date and correct documentation. 
This not only applies to *internal documentation* but also to *external documentation* of software applications the users work with on a daily basis. 
One example for this are modern PLM platforms such as Dassault Systèmes 3DEXPERIENCE. Even though PLM platforms are extremely powerful, 
their documentation is very large and they often lack conversational or guided access to platform knowledge, leading to the following issues when searching for context:
- Hundreds of search results for a single topic
- Difficulty identifying the correct or relevant documentation
- Lack of conversational or guided access to platform knowledge

This project was inspired by these challenges and explores how an agentic AI system 
could support engineers and other stakeholder to quickly access knowledge by:
- Reasoning over documentation sources 
- Iteratively refining answers using critique-based validation
- Providing confidence-aware responses and safe fallbacks

In a production environment, the local document search node could be replaced by:
- An official documentation API
- A secured internal knowledge base
- Enterprise search services



***Important note**  
This repository is a public prototype and does **not** use any internal documentation sources.
Local document retrieval is demonstrated using publicly available PDFs as a stand-in for real documentation sources.





## How to run
```
pip install -r requirements.txt
python main.py
```

**Further notes on running this agent:**

- local_doc_search node
  
  The first step of this agent is to collect information through local document retrieval using FAISS vectorstores built from PDF documentation.
  As described in the *Motivation & Real-World Context* section, this is only a placeholder for an official documentation API

  Therefore, the agent is designed to also operate without locally stored vectorstores:
  - If no vectorstores are present:
    - the local document search step is skipped automatically
    - the agent continues using web-based retrieval
  

  If desired, Llcal document retrieval can be activated as follows: (Optional)
  - Provide your own PDF sources (e.g. public documentation)
  - Update the paths in pdf_vector_storage.py
  - Run the indexing step once:
    
  ```
  python pdf_vector_storage.py
  ```
  After indexing, the agent will automatically incorporate local document context into its workflow.


- safe_file node

  The agent includes a `save_file` node that saves the final answer,
  source references, and agent execution trace to a local text file. This allows to inspect the agent’s reasoning steps.
  The txt file will be stored in the project environment.

