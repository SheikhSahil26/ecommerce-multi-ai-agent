from ecommerce_ai.graph.graph import app_graph


def main():
    result = app_graph.invoke(
        {
            "user_input": "add this thing into cart",
            "intent": "unknown",
            "response": "",
        }
    )

    print(result)


if __name__ == "__main__":
    main()