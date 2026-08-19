import argparse
import os
import sys
from typing import Any

from agentMultiTurnController import multi_turn_graph


def _extract_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(_extract_text(item) for item in content)
    if isinstance(content, dict):
        if "text" in content and isinstance(content["text"], str):
            return content["text"]
        if "content" in content:
            return _extract_text(content["content"])
    return ""


def _render_messages(messages: list[Any]) -> str:
    if not messages:
        return ""

    texts = []
    tool_texts = []
    for message in messages:
        if getattr(message, "type", None) == "ai":
            content = getattr(message, "content", None)
            text = _extract_text(content)
            if text:
                texts.append(text)
            else:
                for tool_call in getattr(message, "tool_calls", []) or []:
                    name = getattr(tool_call, "name", None)
                    if name:
                        tool_texts.append(f"[Transfer action: {name}]")

    if texts:
        return "\n\n".join(texts).strip()
    if tool_texts:
        return "\n".join(tool_texts)

    last_ai = next((m for m in reversed(messages) if getattr(m, "type", None) == "ai"), None)
    if last_ai is not None:
        return repr(getattr(last_ai, "content", None))
    return ""


def run_simulation() -> None:
    sample_inputs = [
        "I am interested in a career in data science.",
        "What courses should I take to prepare?",
        "I might want to switch to product management instead.",
    ]
    history = {"messages": [], "active_agent": "career"}
    for user_input in sample_inputs:
        print(f"User: {user_input}")
        prior_count = len(history.get("messages", []))
        try:
            result = multi_turn_graph.stream([{"role": "user", "content": user_input}], previous=history)
            for chunk in result:
                new_messages = chunk.get("messages", [])[prior_count:]
                history = chunk
                print("Advisor:")
                print(_render_messages(new_messages))
        except Exception as exc:
            print("Advisor:")
            print(f"The advisor could not respond right now: {exc}")
        print("-" * 60)


def run_interactive_chat() -> None:
    history = {"messages": [], "active_agent": "career"}
    print("Type 'exit' or 'quit' to leave the chat.")
    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user_input:
            continue
        prior_count = len(history.get("messages", []))
        try:
            result = multi_turn_graph.stream([{"role": "user", "content": user_input}], previous=history)
            for chunk in result:
                new_messages = chunk.get("messages", [])[prior_count:]
                history = chunk
                print("Advisor:")
                print(_render_messages(new_messages))
        except Exception as exc:
            print("Advisor:")
            print(f"The advisor could not respond right now: {exc}")
        print("-" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    if args.interactive:
        run_interactive_chat()
    else:
        run_simulation()
