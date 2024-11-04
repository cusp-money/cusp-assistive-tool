"""Library to interact with LLM models."""

import logging
import time
from typing import Optional

import vertexai
from vertexai import generative_models


class Model:
    """Base class for LLM."""

    def generate(self, prompt: str) -> str:
        """Returns a generation for prompt."""
        return ""


class Gemini:
    """Gemini model."""

    def __init__(
        self,
        model_name: str = "gemini-1.5-flash-002",
        project: str = "ai-sandbox-399505",
        location: str = "us-central1",
        generation_config: Optional[dict] = None,
    ):
        """Inits the gemini response generator."""
        vertexai.init(project=project, location=location)

        if not generation_config:
            self.generation_config = {
                "temperature": 0,
                "top_p": 0.8,
            }
        else:
            self.generation_config = generation_config
        self.model = generative_models.GenerativeModel(
            model_name,
        )

    def generate(self, prompt: str) -> str:
        """Returns a generation for prompt."""
        start_time = time.time()  # Start timing the request
        responses = self.model.generate_content(
            [prompt],
            generation_config=self.generation_config,
            stream=False,
        )
        duration = (time.time() - start_time) * 1000  # ms
        logging.info(f"Generated llm response in {duration:.2f} ms.")
        return responses.text.strip()
