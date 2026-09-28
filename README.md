# Multi AI Agent E-Commerce API

FastAPI exposes the LangGraph e-commerce agent through a versioned chat endpoint.

## Configure

Copy `.env.example` to `.env` and set `DATABASE_URL` to your PostgreSQL database. Add `LANGSMITH_API_KEY` to enable traces in your LangSmith account. Existing `LANGCHAIN_*` tracing variable names are also supported. Tracing is enabled by default; the project defaults to `multi-ai-agent` unless overridden in `.env`. Keep the API key private.

The agents use Ollama's `gpt-oss:120b-cloud` model. Make sure Ollama is installed, configured, and able to access that model before sending chat requests.

## Run the API

```bash
uv sync
uv run uvicorn ecommerce_ai.main:app --app-dir src --reload
```

- Health: `GET http://localhost:8000/health`
- OpenAPI docs: `http://localhost:8000/docs`
- Chat: `POST http://localhost:8000/api/v1/chat`

Example request:

```json
{
  "message": "Show me laptops under 70000",
  "conversation_id": "optional-stable-conversation-id"
}
```

If `conversation_id` is omitted, the API creates one and returns it. Send that ID with later turns to continue the same in-memory LangGraph conversation. Checkpoints are held in process memory, so conversations reset when the API process restarts.

The response contains `message`, `conversation_id`, `intent`, and `intent_confidence`. Product, shopping/cart, order, and support requests all use the existing supervisor graph.
