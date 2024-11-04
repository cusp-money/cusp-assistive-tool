"""Submodule to handle default scenarios."""

import functools
import logging
from typing import Optional

import fastapi

from utils.speech_processing import audio_streaming_utils, sarvam_ai_utils


@functools.lru_cache(maxsize=10)
def cached_text_to_text(
    input_text: str, target_language_code: str
) -> Optional[str]:
    """Caches audio responses for given input_text."""
    return sarvam_ai_utils.text_to_text(
        input_text=input_text,
        source_language_code="en-IN",
        target_language_code=target_language_code,
    )


@functools.lru_cache(maxsize=10)
def cached_text_to_speech(input_text: str, target_language_code: str):
    """Caches audio responses for given input_text."""
    return sarvam_ai_utils.text_to_speech(
        input_text=input_text,
        target_language_code=target_language_code,
    )


async def send_text_as_audio(
    input_text: str,
    websocket: fastapi.WebSocket,
    stream_sid: str,
    target_language_code: str = "en-IN",
):
    """Sends a text as audio message."""
    # Translate default message to speaker's language if not english.
    if target_language_code != "en-IN":
        translated_text = cached_text_to_text(
            input_text=input_text,
            target_language_code=target_language_code,
        )
        if not translated_text:
            # Defaults to english response when failed to translate.
            translated_text = input_text
            target_language_code = "en-IN"
        input_text = translated_text

    # Convert default text response to speech.
    audio = cached_text_to_speech(
        input_text=input_text, target_language_code=target_language_code
    )
    if not audio:
        logging.error(f"Could not send text={input_text} as audio.")
        return

    # Send audio and wait for twilio to play it
    await audio_streaming_utils.send_audio_to_stream(
        raw_audio_bytes=audio, websocket=websocket, stream_sid=stream_sid
    )

    await audio_streaming_utils.send_mark_event_to_stream(
        websocket=websocket,
        stream_sid=stream_sid,
        mark_tag="default-audio",
    )

    await audio_streaming_utils.wait_for_mark_event(
        websocket=websocket, mark_tag="default-audio"
    )
