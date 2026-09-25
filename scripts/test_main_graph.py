import asyncio

from langchain_core.messages import HumanMessage

from ecommerce_ai.db.database import AsyncSessionLocal
from ecommerce_ai.repositories.product_repository import ProductRepository
from ecommerce_ai.agents.product.graph import create_product_graph
from ecommerce_ai.graph.graph import build_graph
from ecommerce_ai.classifiers.intent_classifier import (
    IntentClassifier,
)


async def main():

    async with AsyncSessionLocal() as session:

        classifier = IntentClassifier()
        # 1. Create repository
        repository = ProductRepository(session)

        # 2. Create Product Graph
        product_graph = create_product_graph(repository)

        # 3. Create Main Graph
        app_graph = build_graph(
            product_graph,
            classifier,
        )

        # 4. User request
        result = await app_graph.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content="hello"
                    )
                ]
            }
        )

        # 5. Print final state
        print("\n" + "=" * 60)
        print("FINAL STATE")
        print("=" * 60)

        print("\nIntent:")
        print(result.get("intent"))

        print("\nMessages:")

        for message in result["messages"]:

            print("\n------------------------------")
            print(type(message).__name__)
            print("------------------------------")

            print(message.content)

            if getattr(message, "tool_calls", None):
                print("\nTool Calls:")
                print(message.tool_calls)


if __name__ == "__main__":
    asyncio.run(main())