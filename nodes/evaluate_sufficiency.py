####################
# Evaluate results #
####################

from langchain_openai import ChatOpenAI
from agent_state import AgentState
import json

# Set up LLM model for evaluation
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

# Define confidence threshold for determining sufficiency of context
confidence_threshold = 0.75


def evaluate_sufficiency(state: AgentState) -> AgentState:

    """
    This function evaluates whether the retrieved context is sufficient to answer the user's question.
    It uses an LLM to assess the context and returns an updated agent state with the evaluation results.
    """
    
    # Retrieve context
    context = "\n\n".join(state["retrieved_context"])

    # Define prompt for evaluation
    prompt = f"""
You are evaluating whether the provided context is sufficient to answer the question.

Rules:
- If the context does NOT allow a clear answer, return answer = "NO_ANSWER"
- Otherwise, provide the best possible answer based ONLY on the context
- Provide a confidence score between 0.0 and 1.0, where 1.0 means absolutely certain and 0.0 means no confidence at all.

Return only valid JSON in the following format:
{{
  "answer": "...",
  "confidence": 0.0
}}

Question:
{state["question"]}

Context:
{context}
"""

    # call LLM to evaluate sufficiency
    llm_call = llm.invoke(prompt).content.strip()

    # If answer is valid JSON, parse it
    try:
        data = json.loads(llm_call)
        answer = data.get("answer")
        confidence = float(data.get("confidence", 0.0))
    except Exception:
        # Safety fallback if parsing fails
        return {
            **state,
            "current_answer": None,
            "confidence": 0.0,
            "done": False,
            "trace": state["trace"] + ["evaluate_sufficiency"],
        }
    
    # If no answer found
    if answer == "NO_ANSWER":
        return {
            **state,
            "current_answer": None,
            "confidence": 0.0,
            "done": False,
            "trace": state["trace"] + ["evaluate_sufficiency"],
            
        }

    # If answer found, update state accordingly
    return {
        **state,
        "current_answer": answer,
        "confidence": confidence,
        "done": confidence >= confidence_threshold,
        "trace": state["trace"] + ["evaluate_sufficiency"],
    }