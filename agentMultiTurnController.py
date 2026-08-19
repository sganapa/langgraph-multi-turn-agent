from typing import Any

from langgraph.checkpoint.memory import MemorySaver

from AgentTaskWrapper import call_career_advisor, call_education_advisor


class MultiTurnGraph:
    def __init__(self) -> None:
        self.memory_saver = MemorySaver()

    def _get_last_ai_message(self, messages: list[Any]) -> Any | None:
        for message in reversed(messages):
            if getattr(message, "type", None) == "ai":
                return message
        return None

    def _contains_transfer_tool_call(self, message: Any) -> bool:
        if not message:
            return False
        tool_calls = getattr(message, "tool_calls", None) or []
        return any(
            getattr(tool_call, "name", None) in {"transfer_to_education_advisor", "transfer_to_career_advisor"}
            for tool_call in tool_calls
        )

    def invoke(self, messages, previous=None):
        conversation_messages = []
        active_agent = "career"

        if previous:
            conversation_messages.extend(previous.get("messages", []))
            active_agent = previous.get("active_agent", active_agent)

        if messages:
            conversation_messages.extend(list(messages))

        while True:
            task = call_career_advisor if active_agent == "career" else call_education_advisor
            response = task(conversation_messages)
            response_messages = response.get("messages", []) if isinstance(response, dict) else []
            conversation_messages.extend(response_messages)

            last_ai_message = self._get_last_ai_message(response_messages)
            if last_ai_message and self._contains_transfer_tool_call(last_ai_message):
                active_agent = "education" if active_agent == "career" else "career"
                continue
            break

        return {"messages": conversation_messages, "active_agent": active_agent}

    def stream(self, messages, previous=None):
        result = self.invoke(messages, previous=previous)
        yield result


multi_turn_graph = MultiTurnGraph()
