# agentic-ai-prototype

## Description
This project implements an agentic AI system using LangGraph that answers software-specific questions by reasoning over different information sources and iteratively improving its answers. The agent follows a stateful workflow, orchestrates based on collected context, tackles halucination by critique-based refinement and safe fallbacks and ensures termination.

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

##Agent architecture:

<img width="487" height="677" alt="architecture" src="https://github.com/user-attachments/assets/20de7b4d-c3e5-4788-97db-0f88f53e7e08" />


## How to run
pip install -r requirements.txt
python main.py
