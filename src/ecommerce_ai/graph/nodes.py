from ecommerce_ai.classifiers.intent_classifier import IntentClassifier
from ecommerce_ai.graph.state import EcommerceState
from langchain_core.messages import AIMessage, HumanMessage


def create_classify_request_node(intent_classifier):

    async def classify_request(state: EcommerceState):

        query = state["messages"][-1].content

        result = await intent_classifier.classify(query)

        intents = result.intents

        tasks = []

        for index, intent in enumerate(intents):
            tasks.append(
                {
                    "task_id": f"task_{index + 1}",
                    "agent": intent,
                    "action": f"{intent}_request",
                    "status": "pending",
                }
            )

        return {
            "original_query": query,
            "intents": intents,
            "planned_tasks": tasks,
            "task_queue": tasks,
            "completed_tasks": [],
            "failed_tasks": [],
            "loop_count": 0,
        }

    return classify_request



def complete_current_task(state: EcommerceState) -> dict:
    task_queue = state.get("task_queue", [])
    current_task = state.get("current_task")
    completed_tasks = state.get("completed_tasks", [])

    if not task_queue or current_task is None:
        return {}

    return {
        "task_queue": task_queue[1:],
        "completed_tasks": [
            *completed_tasks,
            {**current_task, "status": "completed"},
        ],
    }


def supervisor_node(state: EcommerceState) -> dict:

    task_queue = state.get("task_queue", [])

    if not task_queue:
        return {
            "current_task": None,
            "next_worker": "end",
        }

    current_task = task_queue[0]

    return {
        "current_task": current_task,
        "next_worker": current_task["agent"],
    }


def create_product_node(product_graph):

    async def product_node(state: EcommerceState):

        # Execute product agent
        result = await product_graph.ainvoke(
            {"messages": state.get("messages", [])}
        )

        task_queue = state.get("task_queue", [])
        current_task = state.get("current_task")

        # Remove the task that was just completed
        remaining_tasks = task_queue[1:]

        completed_tasks = state.get(
            "completed_tasks",
            []
        )

        completed_task = {
            **current_task,
            "status": "completed",
        }

        new_messages = result.get("messages", [])[len(state.get("messages", [])):]

        return {
            "messages": new_messages,
            "task_queue": remaining_tasks,
            "completed_tasks": [
                *completed_tasks,
                completed_task,
            ],
        }

    return product_node

def create_shopping_node(shopping_graph):

    async def shopping_node(state: EcommerceState):

        # Run shopping agent
        result = await shopping_graph.ainvoke(
            {"messages": state.get("messages", [])}
        )

        # Current task
        task_queue = state.get("task_queue", [])
        current_task = state.get("current_task")

        # Remove completed task
        remaining_tasks = task_queue[1:]

        completed_tasks = state.get(
            "completed_tasks",
            []
        )

        new_messages = result.get("messages", [])[len(state.get("messages", [])):]

        return {
            "messages": new_messages,
            "task_queue": remaining_tasks,
            "completed_tasks": [
                *completed_tasks,
                {
                    **current_task,
                    "status": "completed",
                },
            ],
        }

    return shopping_node

def order_node(state: EcommerceState) -> dict:
    return {
        "messages": [AIMessage(content="Order workflow is not implemented yet.")],
        **complete_current_task(state),
    }


def support_node(state: EcommerceState) -> dict:
    return {
        "messages": [AIMessage(content="Support workflow is not implemented yet.")],
        **complete_current_task(state),
    }


def unknown_node(state: EcommerceState) -> dict:
    return {
        "messages": [AIMessage(content="I could not understand your request.")],
        **complete_current_task(state),
    }
