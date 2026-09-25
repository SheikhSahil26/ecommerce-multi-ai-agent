from langgraph.graph import END, START, StateGraph

from ecommerce_ai.agents.product.graph import create_product_graph
from ecommerce_ai.agents.shopping.graph import create_shopping_graph

from ecommerce_ai.classifiers.intent_classifier import IntentClassifier

from ecommerce_ai.db.database import AsyncSessionLocal

from ecommerce_ai.repositories.product_repository import ProductRepository
from ecommerce_ai.repositories.shopping_repository import ShoppingRepository

from ecommerce_ai.graph.nodes import (
    create_classify_request_node,
    create_product_node,
    create_shopping_node,
    order_node,
    supervisor_node,
    support_node,
    unknown_node,
)

from ecommerce_ai.graph.routers import route_next_task
from ecommerce_ai.graph.state import EcommerceState


def build_graph():

    # --------------------------------------------------
    # Database / repositories
    # --------------------------------------------------

    session = AsyncSessionLocal()

    product_repository = ProductRepository(session)
    shopping_repository = ShoppingRepository(session)


    # --------------------------------------------------
    # Agent graphs
    # --------------------------------------------------

    product_graph = create_product_graph(
        product_repository
    )

    shopping_graph = create_shopping_graph(
        shopping_repository,
        product_repository
    )


    # --------------------------------------------------
    # Intent classifier
    # --------------------------------------------------

    intent_classifier = IntentClassifier()


    # --------------------------------------------------
    # Main LangGraph
    # --------------------------------------------------

    graph = StateGraph(EcommerceState)


    # --------------------------------------------------
    # Nodes
    # --------------------------------------------------

    graph.add_node(
        "classify_request",
        create_classify_request_node(
            intent_classifier
        ),
    )

    graph.add_node(
        "supervisor_node",
        supervisor_node,
    )

    graph.add_node(
        "product",
        create_product_node(
            product_graph
        ),
    )

    graph.add_node(
        "shopping",
        create_shopping_node(
            shopping_graph
        ),
    )

    graph.add_node(
        "order",
        order_node,
    )

    graph.add_node(
        "support",
        support_node,
    )

    graph.add_node(
        "unknown",
        unknown_node,
    )


    # --------------------------------------------------
    # START
    # --------------------------------------------------

    graph.add_edge(
        START,
        "classify_request",
    )


    # --------------------------------------------------
    # Classifier -> Supervisor
    # --------------------------------------------------

    graph.add_edge(
        "classify_request",
        "supervisor_node",
    )


    # --------------------------------------------------
    # Supervisor -> Worker
    # --------------------------------------------------

    graph.add_conditional_edges(
        "supervisor_node",
        route_next_task,
        {
            "product": "product",
            "shopping": "shopping",
            "order": "order",
            "support": "support",
            "unknown": "unknown",
            "end": END,
        },
    )


    # --------------------------------------------------
    # Workers -> Supervisor
    # --------------------------------------------------

    graph.add_edge(
        "product",
        "supervisor_node",
    )

    graph.add_edge(
        "shopping",
        "supervisor_node",
    )

    graph.add_edge(
        "order",
        "supervisor_node",
    )

    graph.add_edge(
        "support",
        "supervisor_node",
    )

    graph.add_edge(
        "unknown",
        "supervisor_node",
    )


    # --------------------------------------------------
    # Compile
    # --------------------------------------------------

    return graph.compile()


# ======================================================
# Main Ecommerce Graph
# ======================================================

app_graph = build_graph()


# ======================================================
# Shopping Agent Graph
# ======================================================

def build_shopping_agent_graph():

    session = AsyncSessionLocal()

    product_repository = ProductRepository(
        session
    )

    shopping_repository = ShoppingRepository(
        session
    )

    return create_shopping_graph(
        shopping_repository,
        product_repository,
    )


shopping_agent_graph = build_shopping_agent_graph()