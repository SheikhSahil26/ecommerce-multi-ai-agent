
from typing import Literal
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel,Field


Intent = Literal[
    "product",
    "shopping",
    "order",
    "support",
    "unknown",
]


class IntentClassification(BaseModel):
    intent: Intent
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

INTENT_CLASSIFICATION_PROMPT = """
You are the intent classifier for an e-commerce application.

Classify the user's request into exactly ONE of these intents:

product:
The user wants to discover, search, browse, compare, or get information
about products.

shopping:
The user wants to buy or purchase something, or perform a shopping action
such as adding/removing/updating cart items, wishlist operations, or checkout.

order:
The user is asking about an existing order, shipment, delivery, or tracking.

support:
The user has a problem, complaint, damaged product, return/refund issue,
or needs customer support.

unknown:
The request does not clearly belong to any category.

Important:
- Do not classify based only on product entities.
- "laptop", "phone", "TV", etc. do NOT automatically mean product.
- Focus on what the user wants to do.

Examples:

"Show me laptops under 70000"
=> {"intent": "product", "confidence": 0.98}

"I want to buy a laptop"
=> {"intent": "shopping", "confidence": 0.95}

"Add this laptop to my cart"
=> {"intent": "shopping", "confidence": 0.99}

"Where is my order?"
=> {"intent": "order", "confidence": 0.99}

"My laptop arrived damaged"
=> {"intent": "support", "confidence": 0.99}

"I need help"
=> {"intent": "unknown", "confidence": 0.60}

IMPORTANT:
Return ONLY valid JSON.

The JSON must have exactly these fields:

{
    "intent": "product | shopping | order | support | unknown",
    "confidence": 0.0
}

Do not use markdown.
Do not use explanations.
Do not return YAML.
Do not return text outside the JSON.
"""


class IntentClassifier:

    def __init__(self):
        self.model = ChatOllama(
            model="gpt-oss:120b-cloud",
            temperature=0,
    )

    def rule_based_classification(
        self,
        text: str,
    ) -> IntentClassification | None:

        text = text.lower().strip()

        # --------------------------------
        # HIGH CONFIDENCE SHOPPING
        # --------------------------------

        shopping_phrases = [
            "add to cart",
            "add this to cart",
            "remove from cart",
            "remove this from cart",
            "show my cart",
            "view my cart",
            "checkout",
            "empty my cart",
            "add to wishlist",
            "remove from wishlist",
        ]

        if any(phrase in text for phrase in shopping_phrases):
            return IntentClassification(
                intent="shopping",
                confidence=0.99,
            )

        # --------------------------------
        # HIGH CONFIDENCE ORDER
        # --------------------------------

        order_phrases = [
            "track my order",
            "where is my order",
            "order status",
            "shipment status",
            "delivery status",
            "track my shipment",
        ]

        if any(phrase in text for phrase in order_phrases):
            return IntentClassification(
                intent="order",
                confidence=0.99,
            )

        # --------------------------------
        # HIGH CONFIDENCE SUPPORT
        # --------------------------------

        support_phrases = [
            "product is damaged",
            "product arrived damaged",
            "received damaged",
            "my product is broken",
            "i have a complaint",
            "i want to complain",
        ]

        if any(phrase in text for phrase in support_phrases):
            return IntentClassification(
                intent="support",
                confidence=0.99,
            )

        # --------------------------------
        # HIGH CONFIDENCE PRODUCT DISCOVERY
        # --------------------------------

        product_phrases = [
            "show me products",
            "show me laptops",
            "show me phones",
            "find products",
            "find laptops",
            "find phones",
            "search for laptops",
            "search for phones",
            "compare products",
            "compare laptops",
            "compare phones",
        ]

        if any(phrase in text for phrase in product_phrases):
            return IntentClassification(
                intent="product",
                confidence=0.99,
            )

        # --------------------------------
        # AMBIGUOUS
        # --------------------------------

        # Returning None means:
        # "Rules could not confidently classify this."
        # Therefore, send it to the LLM.

        return None

    async def classify(
        self,
        text: str,
    ) -> IntentClassification:

    # --------------------------------
    # STEP 1: Rule-based classification
    # --------------------------------

        rule_result = self.rule_based_classification(text)

        if rule_result is not None:

            print(
                f"[INTENT] Rule-based → "
                f"{rule_result.intent} "
                f"(confidence={rule_result.confidence})"
            )

            return rule_result

    # --------------------------------
    # STEP 2: LLM classification
    # --------------------------------

        print("[INTENT] LLM classification")

        response = await self.model.ainvoke(
            [
                SystemMessage(
                    content=INTENT_CLASSIFICATION_PROMPT
                ),
                HumanMessage(
                    content=text
                ),
            ]
        )

        raw_output = response.content

        print(
            f"[INTENT] Raw LLM output:\n"
            f"{raw_output}"
        )

        # --------------------------------
        # STEP 3: Parse JSON
        # --------------------------------

        try:

            data = json.loads(raw_output.strip())

            result = IntentClassification.model_validate(
                data
            )

        except (json.JSONDecodeError, ValueError) as exc:

            print(
                f"[INTENT] Failed to parse LLM output: {exc}"
            )

            return IntentClassification(
                intent="unknown",
                confidence=0.0,
            )

        # --------------------------------
        # STEP 4: Confidence threshold
        # --------------------------------

        print(
            f"[INTENT] LLM → "
            f"{result.intent} "
            f"(confidence={result.confidence})"
        )

        if result.confidence < 0.70:

            print(
                "[INTENT] Low confidence → unknown"
            )

            return IntentClassification(
                intent="unknown",
                confidence=result.confidence,
            )

        return result