"""Helper library for audio streaming."""

import audioop
import base64
import json
import logging
from typing import Optional

import fastapi
import noisereduce
import numpy as np

from constants import voice_assistant_constants


def convert_to_ulaw(raw_audio_bytes: bytes) -> str:
    """Converts the raw audio from PCM format to µ-law format."""
    ulaw_audio = audioop.lin2ulaw(
        raw_audio_bytes, voice_assistant_constants.BYTES_PER_SAMPLE
    )
    audio_base64 = base64.b64encode(ulaw_audio).decode("utf-8")
    return audio_base64


def convert_to_raw_audio_bytes(ulaw_audio: str) -> bytes:
    """Converts the µ-law encoded audio to PCM bytes format ."""
    # Decode the base64 audio data
    ulaw_audio_bytes = base64.b64decode(ulaw_audio)

    # Convert µ-law to raw PCM
    pcm_data = audioop.ulaw2lin(
        ulaw_audio_bytes, voice_assistant_constants.BYTES_PER_SAMPLE
    )
    return pcm_data


def reduce_noise_from_audio(raw_audio_bytes: bytes) -> bytes:
    """Reduces noise from audio."""
    smooth_audio = raw_audio_bytes
    try:
        # Convert bytes to numpy array
        audio_data = np.frombuffer(raw_audio_bytes, np.int16)

        # Set n_fft based on the length of audio data
        n_fft = min(256, len(audio_data))

        smooth_audio = noisereduce.reduce_noise(
            y=audio_data,
            sr=voice_assistant_constants.RATE,
            stationary=True,
            n_fft=n_fft,
            prop_decrease=0.8,
        ).tobytes()
    except Exception as e:  # noqa: E722
        logging.warning(f"Could not reduce noise from audio error {e}.")
    return smooth_audio


async def get_stream_id(websocket: fastapi.WebSocket) -> Optional[str]:
    """Gets the stream id from twilio start event."""
    # Wait for the stream to start
    async for message in websocket.iter_text():
        data = json.loads(message)
        if data.get("event", None) != "start":
            # wait for `start`  event.
            continue
        stream_sid = data["start"]["streamSid"]
        logging.info(f"Received start event from stream {stream_sid}.")
        return stream_sid
    return None


async def wait_for_mark_event(
    websocket: fastapi.WebSocket, mark_tag: str = "ai_message"
):
    """Waits for the mark event to be received."""
    async for message in websocket.iter_text():
        data = json.loads(message)
        if data.get("event", None) != "mark":
            continue
        if data["mark"]["name"] == mark_tag:
            logging.info(f"Received mark event with name: {mark_tag}.")
            break
    return


async def send_audio_to_stream(
    raw_audio_bytes: bytes, websocket: fastapi.WebSocket, stream_sid: str
):
    """Sends audio through websocket connection."""
    encoded_audio = convert_to_ulaw(raw_audio_bytes=raw_audio_bytes)

    message = {
        "event": "media",
        "media": {
            "payload": encoded_audio,
        },
        "streamSid": stream_sid,
    }

    await websocket.send_json(message)
    logging.info("Audio sent.")


async def send_mark_event_to_stream(
    websocket: fastapi.WebSocket, stream_sid: str, mark_tag: str = "ai-message"
):
    """Sends mark event to stream after audio is sent."""
    await websocket.send_json(
        {
            "event": "mark",
            "streamSid": stream_sid,
            "mark": {"name": mark_tag},
        }
    )
    logging.info(f"Sent mark event with tag: {mark_tag}.")
