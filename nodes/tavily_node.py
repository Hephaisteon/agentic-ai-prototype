######################
# Tavily search tool #
######################


from tavily import TavilyClient
from agent_state import AgentState

# Set up Tavily client
tavily = TavilyClient()


def tavily_fallback(state: AgentState) -> AgentState:
    """
    This function provides the final fallback of the agent.
    It provides sources on where to best find the answers to the user question, when no confident answer is found.
    """

    # Retrieve question
    query = state["question"]

    # Perform Tavily search
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    sources = []

    # Extract sources from Tavily response
    for r in response.get("results", []):
        sources.append(f"- {r['title']}: {r['url']}")

    # Define fallback text with sources
    fallback_text = (
        "I could not find a fully supported answer in the available documentation.\n\n"
        "You may find relevant information at the following sources:\n\n"
        + "\n".join(sources)
    )

    # Update state with fallback answer and mark done as True
    return {
        **state,
        "current_answer": fallback_text,
        "done": True,
        "trace": state["trace"] + ["tavily_fallback"],
    }