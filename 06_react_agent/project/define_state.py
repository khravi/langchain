from typing import TypedDict, Annotated, Union
import operator

class AgentState(TypedDict):
    """Defines the state of the agent."""
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    
    