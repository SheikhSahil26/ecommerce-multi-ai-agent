from uuid import uuid4

from fastapi import APIRouter, Depends

from langchain_core.messages import HumanMessage

from ecommerce_ai.api.dependencies import get_main_graph
from ecommerce_ai.graph.state import EcommerceState
from ecommerce_ai.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    graph=Depends(get_main_graph),
):

    conversation_id = (
        request.conversation_id
        or str(uuid4())
    )

    initial_state: EcommerceState = {
        "messages": [
            HumanMessage(
                content=request.message
            )
        ],
        "intent": None,
        "intent_confidence": None,
    }

    result = await graph.ainvoke(
        initial_state
    )

    messages = result["messages"]

    final_message = messages[-1]

    return ChatResponse(
        message=final_message.content,
        conversation_id=conversation_id,
        intent=result.get("intent"),
        intent_confidence=result.get(
            "intent_confidence"
        ),
    )