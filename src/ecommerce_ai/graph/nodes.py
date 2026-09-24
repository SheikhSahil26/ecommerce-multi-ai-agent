from ecommerce_ai.graph.state import EcommerceState


def classify_request(state:EcommerceState)->dict:
    user_input = state["user_input"].lower()

    if any(word in user_input for word in [
        "product",
        "laptop",
        "phone",
        "mobile",
        "computer",
        "price",
        "buy",
    ]):
        return {"intent": "product"}

    if any(word in user_input for word in [
        "cart",
        "add",
        "remove",
        "checkout",
    ]):
        return {"intent": "shopping"}

    if any(word in user_input for word in [
        "order",
        "delivery",
        "track",
        "shipment",
    ]):
        return {"intent": "order"}

    if any(word in user_input for word in [
        "return",
        "refund",
        "damaged",
        "complaint",
        "issue",
    ]):
        return {"intent": "support"}

    return {"intent": "unknown"}



def product_node(state: EcommerceState) -> dict:
    return {
        "response": "Product workflow selected."
    }


def shopping_node(state: EcommerceState) -> dict:
    return {
        "response": "Shopping workflow selected."
    }


def order_node(state: EcommerceState) -> dict:
    return {
        "response": "Order workflow selected."
    }


def support_node(state: EcommerceState) -> dict:
    return {
        "response": "Support workflow selected."
    }


def unknown_node(state: EcommerceState) -> dict:
    return {
        "response": "I could not understand the request."
    }