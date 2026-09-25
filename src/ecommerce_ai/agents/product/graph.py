from langchain_core.messages import SystemMessage

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from ecommerce_ai.agents.product.agent import create_product_agent
from ecommerce_ai.agents.product.prompts import (
    PRODUCT_AGENT_SYSTEM_PROMPT,
)
from ecommerce_ai.agents.product.state import ProductAgentState
from ecommerce_ai.repositories.product_repository import ProductRepository


def create_product_graph(
    repository: ProductRepository,
):

    # --------------------------------
    # Create Product Agent
    # --------------------------------

    model, tools = create_product_agent(repository)

    # --------------------------------
    # Create Tool Node
    # --------------------------------

    tool_node = ToolNode(tools)

    # --------------------------------
    # LLM Node
    # --------------------------------

    async def product_llm(
        state: ProductAgentState,
    ):

        messages = state["messages"]

        messages_with_system_prompt = [
            SystemMessage(
                content=PRODUCT_AGENT_SYSTEM_PROMPT
            ),
            *messages,
        ]

        response = await model.ainvoke(
            messages_with_system_prompt
        )

        return {
            "messages": [response]
        }

    # --------------------------------
    # Router
    # --------------------------------

    def should_continue(
        state: ProductAgentState,
    ):

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "tools"

        return END

    # --------------------------------
    # Create Graph
    # --------------------------------

    graph = StateGraph(ProductAgentState)

    # --------------------------------
    # Add Nodes
    # --------------------------------

    graph.add_node(
        "product_llm",
        product_llm,
    )

    graph.add_node(
        "product_tools",
        tool_node,
    )

    # --------------------------------
    # START → LLM
    # --------------------------------

    graph.add_edge(
        START,
        "product_llm",
    )

    # --------------------------------
    # LLM → Tool OR END
    # --------------------------------

    graph.add_conditional_edges(
        "product_llm",
        should_continue,
        {
            "tools": "product_tools",
            END: END,
        },
    )

    # --------------------------------
    # Tool → LLM
    # --------------------------------

    graph.add_edge(
        "product_tools",
        "product_llm",
    )

    # --------------------------------
    # Compile
    # --------------------------------

    return graph.compile()