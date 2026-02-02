################
# Improve_node #
################


# set up openai api key
# export OPENAI_API_KEY="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"

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from agent_state import AgentState

# Set up LLM model for improvement node
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)


def improvement_search(state: AgentState) -> AgentState:
    """
    Improving the current answer based on the critique provided.
    """

    # Fallback if no critique is passed! --> No improvement needed
    if not state["retrieved_critique"]:
        return {
            **state,
            "iteration": state["iteration"] + 1,
            "trace": state["trace"] + ["improve"],
        }

    # Retrieve question, current answer, and critique
    query = state["question"]
    cur_answer = state.get("current_answer")
    cur_critic = state["retrieved_critique"][-1]

    # Define prompt for improvement node
    prompt = f"""
You are a Dassault Engineer specialistin 3DExperience. You have the following information about a 3DX related question:

Question:
{query}

Answer:
{cur_answer}

A colleague has reviewed this answer and provided the following critique: 
{cur_critic}

Refine the answer based on the critique and provide additional factual information to support it.
"""

    # call LLM to perform improvement search
    web_results = llm.invoke(prompt).content

    # update state with improved answer
    return {
        **state,
        "retrieved_context": state["retrieved_context"] + [web_results],
        "messages": state["messages"] + [AIMessage(content=web_results)],
        "iteration": state["iteration"] + 1,
        "trace": state["trace"] + ["improve"],
    }

