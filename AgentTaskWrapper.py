from langchain_core.messages import AIMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from agent_definitions import career_advisor, education_advisor


def _fallback_response(message: str):
    return {"messages": [AIMessage(content=message)]}


def call_career_advisor(messages):
    try:
        return career_advisor.invoke({"messages": list(messages or [])})
    except ChatGoogleGenerativeAIError as exc:
        return _fallback_response(
            f"The Gemini API is currently unavailable ({exc}). Please try again later or use a different API key."
        )
    except Exception as exc:
        return _fallback_response(f"The advisor could not respond right now: {exc}")


def call_education_advisor(messages):
    try:
        return education_advisor.invoke({"messages": list(messages or [])})
    except ChatGoogleGenerativeAIError as exc:
        return _fallback_response(
            f"The Gemini API is currently unavailable ({exc}). Please try again later or use a different API key."
        )
    except Exception as exc:
        return _fallback_response(f"The advisor could not respond right now: {exc}")
