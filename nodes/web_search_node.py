###################
# web search node
###################

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from agent_state import AgentState

# Set up LLM model for web search
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)


def web_search(state: AgentState) -> AgentState:
    """
    Perform web search using the LLM and update the agent state with retrieved context and messages.
    """

    # retrieve question from state
    query = state["question"]

    # Define prompt for web search
    prompt = f"""
Search the web and extract factual information to answer the question below.
Focus on official documentation, vendor sources, or authoritative references.

Question:
{query}

Return ONLY relevant factual information.
Do NOT answer the question directly.
"""

    # call LLM to perform web search
    web_results = llm.invoke(prompt).content

    # update state with web results
    return {
        **state,
        "retrieved_context": state["retrieved_context"] + [web_results],
        "messages": state["messages"] + [AIMessage(content=web_results)],
        "iteration": state["iteration"] + 1,
        "web_search_done": True,
        "trace": state["trace"] + ["web_search"],
    }

