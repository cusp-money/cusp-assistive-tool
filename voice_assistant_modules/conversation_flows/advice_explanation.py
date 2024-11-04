"""Submodule to handle conversation around advisor's notes with human."""

from typing import Optional

from langchain_core import prompts

from constants.prompts import ria_advice_explanation_prompt
from utils.text_processing import llm_utils
from voice_assistant_modules.conversation_flows import base_conversation_flow


class AdviceExplanationConversation(
    base_conversation_flow.BaseConversationFlow
):
    """Handles conversation with human regarding RIA's advice."""

    def __init__(
        self,
        customer_profile_and_advice: Optional[str] = "",
    ):
        """Initiate RIA's advice explanation conversation flow."""
        self.prompt = prompts.ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    ria_advice_explanation_prompt.PROMPT,
                ),
                prompts.MessagesPlaceholder(variable_name="chat_history"),
            ]
        )

        self.customer_profile_and_advice = customer_profile_and_advice
        self.model = llm_utils.Gemini()
        self.conversation_ended = False

    def generate_response(self) -> Optional[str]:
        """Generates the ai response based on current chat history."""
        # Add values for placeholders in the  prompt template.
        prompt_text = self.prompt.format(
            chat_history=self.chat_history,
            customer_profile_and_advice=self.customer_profile_and_advice,
        )

        # Generate model response
        ai_response = self.model.generate(prompt=prompt_text)
        if not ai_response:
            ai_response = (
                "Sorry, I totally missed that. Can you please repeat?"
            )

        if ai_response.lower().startswith("ai:"):
            ai_response = ai_response[3:]

        self.add_ai_message(ai_response)  # Add ai message in chat history
        return ai_response

    def is_conversation_ended(self) -> bool:
        """Ends the conversation if user do not have any more questions."""
        return self.conversation_ended
