from ecommerce_ai.graph.state import EcommerceState


def route_request(state: EcommerceState) -> str:
    return state["intent"]