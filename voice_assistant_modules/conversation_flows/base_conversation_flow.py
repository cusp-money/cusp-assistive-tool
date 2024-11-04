"""Base class for human and ai conversation flows."""

from langchain_core import messages


class BaseConversationFlow:
    """Base conversation flow."""

    chat_history: list[messages.BaseMessage] = []

    def add_human_message(self, text: str):
        """Appends a human message to chat history."""
        self.chat_history.append(messages.HumanMessage(content=text))

    def add_ai_message(self, text: str):
        """Appends an AI message to chat history."""
        self.chat_history.append(messages.AIMessage(content=text))

    def generate_response(self) -> str:
        """Generates next ai response based on chat history."""
        raise NotImplementedError

    def is_conversation_ended(self) -> bool:
        """Checks if conversation is already ended."""
        raise NotImplementedError
