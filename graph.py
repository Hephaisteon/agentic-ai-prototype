######################
# Building the Graph #
######################


from langgraph.graph import StateGraph, END
from agent_state import AgentState
from node_local_doc_search import local_docs_search
from evaluate_sufficiency import evaluate_sufficiency
from web_search_node import web_search
from critic_node import critic
from improve_node import improvement_search
from tavily_node import tavily_fallback
from save_file import save_to_file


# Define maximum iterations to prevent infinite agent loops
MAX_ITERATIONS = 4


def sufficiency_router(state: AgentState):
    """
    Central routing logic in the evaluate_sufficiency node.
    """

    # if state is done --> save file
    if state["done"]:
        return "save_file"
    
    # if max iterations reached --> tavily fallback
    if state["iteration"] >= MAX_ITERATIONS:
        return "tavily_fallback"
    
    # if no current answer
    if state.get("current_answer") is None:
        # if web search not done --> web search (avoid multiple web searches)
        if not state["web_search_done"]:
            return "web_search"
        # else --> critic
        else:
            return "critic"

    return "critic"



def critic_router(state: AgentState):
    """
    Central routing logic in the critic node.
    
    If critique has been added, go to improve node
    else --> go to tavily fallback.
    """

    if state["critique_added"]:
        return "improve"

    return "tavily_fallback"



def build_graph():

    """
    This function builds and compiles the state graph for the agent.
    """

    # Initialize state graph
    graph = StateGraph(AgentState)

    # Define nodes
    graph.add_node("local_docs_search", local_docs_search)
    graph.add_node("evaluate_sufficiency", evaluate_sufficiency)
    graph.add_node("web_search", web_search)
    graph.add_node("critic", critic)
    graph.add_node("improve", improvement_search)
    graph.add_node("tavily_fallback", tavily_fallback)
    graph.add_node("save_file", save_to_file)

    # Define entry point
    graph.set_entry_point("local_docs_search")

    # local docs search always goes to evaluate sufficiency
    graph.add_edge("local_docs_search", "evaluate_sufficiency")


    # 1. decision point - evaluate_sufficiency
    graph.add_conditional_edges(
        "evaluate_sufficiency",
        sufficiency_router,
        {
            "save_file": "save_file",
            "web_search": "web_search",
            "tavily_fallback": "tavily_fallback",
            "critic": "critic",
        },
    )

    # web search always goes to evaluate sufficiency
    graph.add_edge("web_search", "evaluate_sufficiency")


    # 2. decision point - critic
    graph.add_conditional_edges(
        "critic",
        critic_router,
        {
            "tavily_fallback": "tavily_fallback",
            "improve": "improve",
        },
    )

    
    # improvements are always evaluated
    graph.add_edge("improve", "evaluate_sufficiency")


    # Tavily always goes to save file 
    graph.add_edge("tavily_fallback", "save_file")

    # save file always ends the graph
    graph.add_edge("save_file", END)


    return graph.compile()


