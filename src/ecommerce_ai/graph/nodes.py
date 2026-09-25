from ecommerce_ai.classifiers.intent_classifier import IntentClassifier
from ecommerce_ai.graph.state import EcommerceState
from langchain_core.messages import AIMessage, HumanMessage


def create_classify_request_node(
    classifier: IntentClassifier,
):
    async def classify_request(
        state: EcommerceState,
    ) -> dict:

        user_input = state["messages"][-1].content

        result = await classifier.classify(user_input)

        return {
            "intent": result.intent,
        }

    return classify_request


def create_product_node(product_graph):

    async def product_node(
        state: EcommerceState,
    ) -> dict:

        existing_messages = state["messages"]

        result = await product_graph.ainvoke(
            {
                "messages": existing_messages
            }
        )

        new_messages = result["messages"][
            len(existing_messages):
        ]

        return {
            "messages": new_messages
        }

    return product_node


def shopping_node(state: EcommerceState) -> dict:
    return {
        "messages": [
            AIMessage(
                content="Shopping workflow is not implemented yet."
            )
        ]
    }
def order_node(state: EcommerceState) -> dict:
    return {
        "messages": [
            AIMessage(
                content="Order workflow is not implemented yet."
            )
        ]
    }

def support_node(state: EcommerceState) -> dict:
    return {
        "messages": [
            AIMessage(
                content="Support workflow is not implemented yet."
            )
        ]
    }

def unknown_node(state: EcommerceState) -> dict:
    return {
        "messages": [
            AIMessage(
                content="I could not understand your request."
            )
        ]
    }