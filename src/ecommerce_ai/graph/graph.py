from langgraph.graph import END, START, StateGraph

from ecommerce_ai.graph.nodes import (
    classify_request,
    order_node,
    product_node,
    shopping_node,
    support_node,
    unknown_node,
)
from ecommerce_ai.graph.routers import route_request
from ecommerce_ai.graph.state import EcommerceState

def build_graph():
    graph = StateGraph(EcommerceState)

    #add nodes 
    graph.add_node("classify_request", classify_request)
    graph.add_node("product", product_node)
    graph.add_node("shopping", shopping_node)
    graph.add_node("order", order_node)
    graph.add_node("support", support_node)
    graph.add_node("unknown", unknown_node)

    # START -> classifier
    graph.add_edge(START, "classify_request")

    # Classifier -> router -> appropriate workflow
    graph.add_conditional_edges(
        "classify_request",
        route_request,
        {
            "product": "product",
            "shopping": "shopping",
            "order": "order",
            "support": "support",
            "unknown": "unknown",
        },
    )

    # Workflow nodes -> END
    graph.add_edge("product", END)
    graph.add_edge("shopping", END)
    graph.add_edge("order", END)
    graph.add_edge("support", END)
    graph.add_edge("unknown", END)

    return graph.compile()


app_graph = build_graph()