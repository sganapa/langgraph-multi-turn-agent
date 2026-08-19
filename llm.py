import getpass
import os
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI


def get_model(model_name: Optional[str] = None, api_key: Optional[str] = None):
    resolved_api_key = api_key or os.getenv("GOOGLE_API_KEY")

    if not resolved_api_key:
        print("GOOGLE_API_KEY was not found in the environment.")
        resolved_api_key = getpass.getpass("Enter your Google API key: ")
        if resolved_api_key:
            os.environ["GOOGLE_API_KEY"] = resolved_api_key

    if not resolved_api_key:
        raise RuntimeError("A Google API key is required to run the application.")

    resolved_model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

    return ChatGoogleGenerativeAI(
        model=resolved_model_name,
        google_api_key=resolved_api_key,
    )
