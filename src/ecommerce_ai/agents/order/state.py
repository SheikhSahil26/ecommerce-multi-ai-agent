from langgraph.graph import MessagesState


class OrderAgentState(MessagesState, total=False):
    tool_call_count: int
    tool_limit_reached: bool
