"""Submodule to handle conversation around advisor questionnaire with human."""

import ast
import re
from typing import Any, Optional

import pandas as pd
from langchain_core import prompts
from vertexai import generative_models

from constants import customer_profile_doc
from constants.prompts import advisor_questionnaire_prompt
from utils import google_docs_utils
from utils.text_processing import llm_utils
from voice_assistant_modules.conversation_flows import base_conversation_flow


class AdvisorQuestionnaireConversation(
    base_conversation_flow.BaseConversationFlow
):
    """Handles conversation to get answers of advisor's question from human."""

    def __init__(
        self, questionnaire: list[dict], aa_summary: Optional[str] = ""
    ):
        """Initiate advisor questionnaire conversation flow."""
        self.ai_response_key = "next_ai_response_for_human"
        self.prompt = prompts.ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    advisor_questionnaire_prompt.PROMPT,
                ),
                prompts.MessagesPlaceholder(variable_name="chat_history"),
            ]
        )
        self.questionnaire = questionnaire
        self.question_ids = self._get_question_ids(questionnaire=questionnaire)

        self.model = llm_utils.Gemini(
            generation_config=self._get_structured_generation_config(
                required_properties=self.question_ids
            )
        )
        self.aa_summary = self._build_aa_summary(aa_summary=aa_summary)
        self.latest_answers = dict()

    def generate_response(self) -> Optional[str]:
        """Generates the ai response based on current chat history."""
        # Add values for placeholders in the  prompt template.
        prompt_text = self.prompt.format(
            chat_history=self.chat_history,
            questions=self._build_question_md(),
            aa_summary=self.aa_summary,
        )

        # Generate model response
        structured_response_str = self.model.generate(prompt=prompt_text)
        structured_response = ast.literal_eval(structured_response_str)

        # Get ai response from the structured response.
        ai_response = structured_response.pop(self.ai_response_key)
        if not ai_response:
            ai_response = (
                "Sorry, I totally missed that. Can you please repeat?"
            )

        # Update latest answers
        self.latest_answers = structured_response

        # End the conversation if all the answers has been provided.
        if self.is_conversation_ended():
            ai_response = (
                "Thanks for your help. I think we have got all the answers "
                "required at the moment. Our registered investment advisor "
                "will soon provide the advise. Have a nice day. "
            )

        self.add_ai_message(ai_response)  # Add ai message in chat history
        return ai_response

    def save_answer_to_doc(self, doc_id: str, docs_service: Any, creds: Any):
        """Writes answers collected from the conversation to google doc."""
        creds, docs_service, drive_service = (
            google_docs_utils.get_google_doc_creds()
        )
        # Add a heading and description for customer profile
        google_docs_utils.write_heading_to_google_doc(
            doc_id=doc_id,
            docs_service=docs_service,
            heading=customer_profile_doc.CUSTOMER_PROFILE_HEADING,
            heading_level=1,
        )
        google_docs_utils.write_title_to_google_doc(
            doc_id=doc_id,
            docs_service=docs_service,
            title=customer_profile_doc.CUSTOMER_PROFILE_DESCRIPTION,
        )

        # Add answers table
        question_answer_list = []
        for question in self.questionnaire:
            answer = self.latest_answers.get(question["index"], "")
            question_answer_list.append([question["question"], answer])

        google_docs_utils.write_table_to_google_doc(
            table_data=question_answer_list,
            doc_id=doc_id,
            docs_service=docs_service,
            creds=creds,
        )

        # Add a heading and description for financial advisor blank section
        google_docs_utils.write_heading_to_google_doc(
            doc_id=doc_id,
            docs_service=docs_service,
            heading=customer_profile_doc.FINANCIAL_ADVISE_HEADING,
            heading_level=1,
        )
        google_docs_utils.write_title_to_google_doc(
            doc_id=doc_id,
            docs_service=docs_service,
            title=customer_profile_doc.FINANCIAL_ADVISE_DESCRIPTION,
        )

    def is_conversation_ended(self) -> bool:
        """Ends the conversation if all questions are answered."""
        if len(self.latest_answers.values()) != 0:
            tmp_list = [
                ele for ele in self.latest_answers.values() if ele == ""
            ]
            if len(tmp_list) == 0:
                return True

        return False

    def _get_question_ids(self, questionnaire: list[dict]):
        """Gets the question ids from questionnaire."""
        return [question["index"] for question in questionnaire]

    def _get_structured_generation_config(
        self, required_properties: list[str]
    ):
        """Returns a generation config to get structured output from gemini."""
        properties = {
            key: {
                "type": "string",
            }
            for key in required_properties + [self.ai_response_key]
        }
        gen_config = generative_models.GenerationConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": properties,
                "required": required_properties,
            },
        )
        return gen_config

    def _build_question_md(self):
        """Renders questions and received answers as markdown table."""
        # Convert questions and answers to markdown table.
        qa_df = pd.DataFrame(data=self.questionnaire)
        qa_df.set_index("index", inplace=True)
        qa_df["answers"] = [
            self.latest_answers.get(question_id, "")
            for question_id in self.question_ids
        ]
        qa_md = qa_df.to_markdown()

        # Clean markdown.
        re_combine_lines = re.compile(r"---+")
        re_combine_whitespace = re.compile(r" +")

        qa_md = re_combine_lines.sub("---", qa_md)
        qa_md = re_combine_whitespace.sub(" ", qa_md)

        return qa_md

    def _build_aa_summary(self, aa_summary: str):
        if not aa_summary:
            return ""

        aa_desc = customer_profile_doc.AA_SUMMARY_DESCRIPTION

        if aa_desc in aa_summary:
            start_index = aa_summary.index(aa_desc)
            return aa_summary[start_index + len(aa_desc) :]

        return aa_summary
