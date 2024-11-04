"""Helper library to consume SarvamAI's speech processing APIs."""

import base64
import io
import logging
import wave
from typing import Optional

from constants import voice_assistant_constants
from utils import api_utils
from voice_assistant_modules.conversation_flows import base_conversation_flow


def chunk_text(text: str, max_length: int = 450) -> list[str]:
    """Chunks text into a list of 500-character chunks."""
    if len(text) < max_length:
        return [text]
    words = text.split()  # Split by words to avoid splitting mid-word
    chunks = []
    current_chunk = []

    # Create chunks with max_length characters
    for word in words:
        # If adding the next word exceeds max_length, save the current chunk
        # and start a new one
        if len(" ".join(current_chunk + [word])) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def text_to_speech(
    input_text: str, target_language_code: str
) -> Optional[bytes]:
    """Converts text string into speech in target language."""
    payload = {
        "inputs": chunk_text(text=input_text)[:3],  # API supports max 3 chunks
        "target_language_code": target_language_code,
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.1,
        "loudness": 1.5,
        "speech_sample_rate": voice_assistant_constants.RATE,
        "enable_preprocessing": True,
        "model": "bulbul:v1",
    }

    headers = {
        "API-Subscription-Key": voice_assistant_constants.SARVAM_API_KEY
    }

    response = api_utils.make_request(
        base_url=voice_assistant_constants.SARVAM_BASE_URL,
        method="POST",
        endpoint="text-to-speech",
        headers=headers,
        payload=payload,
    )

    if response and "audios" in response:
        audio_base64 = "".join(response["audios"])
        audio_data = base64.b64decode(audio_base64)
        return audio_data
    logging.error(f"Unable to convert text to speech for input {input_text}.")
    return None


def text_to_text(
    input_text: str,
    source_language_code: str,
    target_language_code: str,
) -> Optional[str]:
    """Translates text to target language text."""
    payload = {
        "input": input_text,
        "source_language_code": source_language_code,
        "target_language_code": target_language_code,
        "speaker_gender": "Female",
        "mode": "code-mixed",
        "model": "mayura:v1",
        "enable_preprocessing": False,
    }

    headers = {
        "API-Subscription-Key": voice_assistant_constants.SARVAM_API_KEY
    }

    response = api_utils.make_request(
        base_url=voice_assistant_constants.SARVAM_BASE_URL,
        method="POST",
        endpoint="translate",
        headers=headers,
        payload=payload,
    )

    if response and "translated_text" in response:
        return response["translated_text"]
    logging.error(f"Unable to translate text for input {input_text}.")
    return None


def speech_to_text_translate(
    audio_data: bytes,
) -> Optional[tuple[str, str]]:
    """Translates speech from any reginal language to english text."""
    # Wrap the raw audio bytes in a BytesIO buffer to structure it as a WAV file
    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, "wb") as wf:
        wf.setnchannels(voice_assistant_constants.CHANNELS)
        wf.setsampwidth(voice_assistant_constants.BYTES_PER_SAMPLE)
        wf.setframerate(voice_assistant_constants.RATE)
        wf.writeframes(audio_data)

    # Move the buffer's pointer to the beginning for reading
    audio_buffer.seek(0)

    files = {"file": ("audio.wav", audio_buffer, "audio/wav")}

    headers = {
        "API-Subscription-Key": voice_assistant_constants.SARVAM_API_KEY
    }

    response = api_utils.make_request(
        base_url=voice_assistant_constants.SARVAM_BASE_URL,
        method="POST",
        endpoint="speech-to-text-translate",
        headers=headers,
        files=files,
    )

    if response and "transcript" in response and "language_code" in response:
        return response["transcript"], response["language_code"]
    return None


def speech_to_speech(
    raw_audio_bytes: bytes,
    conversation_flow_handler: base_conversation_flow.BaseConversationFlow,
) -> Optional[tuple[bytes, bool]]:
    """Generates ai speech response for user speech."""
    # Transcribe input audio to english text.
    response = speech_to_text_translate(audio_data=raw_audio_bytes)
    if not response:
        return response
    transcript, language_code = response

    # Using default language when speaker's language cannot be determined.
    if language_code is None:
        language_code = voice_assistant_constants.DEFAULT_AI_LANGUAGE

    if not transcript:
        logging.error("Empty transcript found.")
        return None

    # Generate AI response for given human input.
    conversation_flow_handler.add_human_message(text=transcript)
    ai_message = conversation_flow_handler.generate_response()
    if not ai_message:
        return None

    # Translate ai response to speaker's language if not english.
    if language_code != "en-IN":
        translated_text = text_to_text(
            input_text=ai_message,
            source_language_code="en-IN",
            target_language_code=language_code,
        )
        if not translated_text:
            # Defaults to english response when failed to translate.
            translated_text = ai_message
            language_code = "en-IN"

    # Transcribe ai response to speech in target language
    output_audio = text_to_speech(
        input_text=translated_text,
        target_language_code=language_code,
    )

    return output_audio
