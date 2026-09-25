from typing import Literal

from langgraph.graph import MessagesState


class EcommerceState(MessagesState):
    intent: Literal[
        "product",
        "shopping",
        "order",
        "support",
        "unknown",
    ] | None