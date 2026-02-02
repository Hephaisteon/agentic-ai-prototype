################################
# Node - local document search #
################################


from langchain_core.messages import AIMessage
from agent_state import AgentState
from local_search import search_local_docs, vector_stores


def local_docs_search(state: AgentState) -> AgentState:
    """
    Function to perform local document search node.

    The function uses pre-built, locally stored, vectorstores to search for relevant
    documentation chunks based on the user's question, and updates the
    agent state with the retrieved context and messages.
    """

    # If no vectorstores available --> skip PDF search node
    if not vector_stores:
        return {
            **state,
            "trace": state["trace"] + ["local_docs_search (skipped)"],
        }

    # Perform local document search with the user question
    query = state["question"]
    results = search_local_docs(query)

    # If no results found --> continue without updating context
    if not results.strip():
        return {
            **state,
            "trace": state["trace"] + ["local_docs_search (no results)"],
        }

    # If results found, append context, messages and trace
    return {
        **state,
        "retrieved_context": state["retrieved_context"] + [results],
        "messages": state["messages"] + [AIMessage(content=results)],
        "trace": state["trace"] + ["local_docs_search"],
    }
