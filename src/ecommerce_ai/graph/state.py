from typing import Literal, TypedDict


class EcommerceState(TypedDict):
    user_input: str
    intent: Literal[
        "product",
        "shopping",
        "order",
        "support",
        "unknown",
    ]
    response: str