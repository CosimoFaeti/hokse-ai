from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from src.domain.entities.agent_state_entity import AgentState
from src.domain.utilities.logger import logger
from src.infrastructure.nodes.nodes import make_model_node
from src.infrastructure.utils.logic_graph import should_continue

def build_graph(model: BaseChatModel, tools: list[BaseTool]):
    """"""
    logger.info(msg="Start")
    logger.debug(msg=f"Building graph with {len(tools)} tools")

    model_with_tools = model.bind_tools(tools)

    model_node = make_model_node(model_with_tools)
    tool_node = ToolNode(tools)

    # Build workflow
    agent_builder = StateGraph(AgentState)

    # Add nodes
    agent_builder.add_node("llm_call", model_node)
    agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        {"tool_node": "tool_node", END: END}
    )
    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent
    return agent_builder.compile()


