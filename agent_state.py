######################
# Define Agent State #
######################

from typing import TypedDict, Sequence, Optional
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage


class AgentState(TypedDict):

    """
    Define the structure of the agent's state using TypedDict.
    """

    # Original user question
    question: str 

    # Conversation + reasoning trace (append-only)
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # Retrieved knowledge chunks for context
    retrieved_context: Sequence[str]

    # Retrieved critic elements
    retrieved_critique: Sequence[str]

    # whether critique has been added
    critique_added: bool

    # Latest candidate answer (if any)
    current_answer: Optional[str]

    # Confidence score used for routing decisions
    confidence: Optional[float]

    # Iteration counter (prevents infinite loops)
    iteration: int

    # Whether web search has been performed
    web_search_done: bool

    # Whether the graph should stop
    done: bool

    # store trace of the agent
    trace: list[str]



def create_initial_state(question: str) -> AgentState:
    """
    Function to create the initial state of the agent given a user question.
    """


    return {
        "question": question,
        "messages": [HumanMessage(content=question)],
        "retrieved_context": [],
        "retrieved_critique": [],
        "critique_added": False,
        "current_answer": None,
        "confidence": None,
        "iteration": 0,
        "web_search_done": False,
        "done": False,
        "trace": [],
    }

