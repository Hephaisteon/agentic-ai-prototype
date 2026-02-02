######################
# Define Critic node #
######################

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from agent_state import AgentState

# Set up LLM model for critic
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)


def critic(state: AgentState) -> AgentState:
    """
    This function critically evaluates the current answer against the retrieved context.

    If the answer is fully supported by the context, it marks the critique_added attribute of the agent state as not added.
    If there are gaps or inaccuracies, it generates critique points and updates the agent state.
    """

    # Retrieve current answer and context
    answer = state.get("current_answer")
    context = "\n\n".join(state["retrieved_context"])

    # Define prompt for critique
    prompt = f"""

        You are a 3DX Expert and a critical reviewer.

        Question:
        {state["question"]}

        Proposed Answer:
        {answer}

        Context:
        {context}

        Determine whether or not the proposed answer is fully supported by the provided context.
        Please answer as follows:
        
        - If the answer fully supported by the context?

        Answer with:
        APPROVED

        - If the answer lacks support from the context or has inaccuracies, 
        
        Formulate:
        concise critique bullet points

        """

    # call LLM to determine if critique is needed
    verdict = llm.invoke(prompt).content.strip()

    # If no critique found, mark critique_added as False
    if verdict == "APPROVED":
        return {
            **state,
            "critique_added": False,
            "done": False,
            "trace": state["trace"] + ["critic"],
        }

    # Otherwise, add critique to retrieved_critique and mark critique_added as True
    else:
        return {
            **state,
            "retrieved_critique": state.get("retrieved_critique", []) + [verdict],
            "critique_added": True,
            "messages": state["messages"] + [AIMessage(content=verdict)],
            "done": False,
            "trace": state["trace"] + ["critic"],
        }