##################
# Agent registry #
##################

from typing import Callable, Dict

# Type alias for clarity
AgentFn = Callable[[dict], dict]

# Registry to hold agent functions
agent_registry: Dict[str, AgentFn] = {}

def register_agent(name: str, agent_fn: AgentFn):
    """
    This function registers an agent function under a given name. 
    """
    agent_registry[name] = agent_fn


def get_agent(name: str) -> AgentFn:
    """
    This function retrieves a registered agent function by name.
    """

    # Check if agent exists
    if name not in agent_registry:
        raise ValueError(f"Agent '{name}' not found in registry")
    return agent_registry[name]