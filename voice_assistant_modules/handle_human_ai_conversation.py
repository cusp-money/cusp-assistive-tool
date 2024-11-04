"""Submodule for human and AI conversation over a phone call."""

import asyncio
import json
import logging
from collections import defaultdict

import fastapi

from constants import voice_assistant_constants
from utils.speech_processing import (
    audio_streaming_utils,
    sarvam_ai_utils,
    voice_activity_detection,
)
from voice_assistant_modules.conversation_flows import base_conversation_flow

SpeakerState = voice_activity_detection.SpeakerState

# Mapping from phone number to ai thinking state.
is_ai_thinking = defaultdict(bool)

# Mapping from phone number to caller's listening state.
is_client_listening_to_ai = defaultdict(bool)

# Mapping from phone number to conversation state.
is_conversation_ended = defaultdict(bool)

# Mapping from phone number to received speech chunks.
client_audio_buffers = defaultdict(list)


async def send_to_twilio(
    websocket: fastapi.WebSocket,
    phone_number: str,
    stream_id: str,
    conversation_flow_handler: base_conversation_flow.BaseConversationFlow,
):
    """Processes received audio chunks and sends audio back to Twilio."""
    try:
        while True:
            if is_conversation_ended[phone_number]:
                break

            # Do nothing when speaker is still speaking.
            if not is_ai_thinking[phone_number]:
                await asyncio.sleep(0.1)  # Sleep if inactive
                continue

            # Combine spoken audio chunks.
            raw_audio_bytes = b"".join(client_audio_buffers[phone_number])

            # Process speech if available and send audio response back
            if (
                raw_audio_bytes
                and len(raw_audio_bytes)
                > voice_assistant_constants.SPEECH_PROCESSING_MIN_BYTES
            ):
                # Reset buffer
                client_audio_buffers[phone_number] = []

                # Generate AI audio response.
                output_audio = sarvam_ai_utils.speech_to_speech(
                    raw_audio_bytes=raw_audio_bytes,
                    conversation_flow_handler=conversation_flow_handler,
                )
                if not output_audio:
                    is_ai_thinking[phone_number] = False
                    continue
                is_conversation_ended[phone_number] = (
                    conversation_flow_handler.is_conversation_ended()
                )

                # Send generated audio audio back to caller
                await audio_streaming_utils.send_audio_to_stream(
                    raw_audio_bytes=output_audio,
                    websocket=websocket,
                    stream_sid=stream_id,
                )

                await audio_streaming_utils.send_mark_event_to_stream(
                    websocket=websocket,
                    stream_sid=stream_id,
                )

                is_client_listening_to_ai[phone_number] = True

            # If no audio is being played then mark ai as idle.
            if not is_client_listening_to_ai[phone_number]:
                is_ai_thinking[phone_number] = False

            await asyncio.sleep(0.1)  # Sleep if inactive

    except Exception as e:
        logging.error(f"Error while sending audio to twilio : {e}")


async def receive_from_twilio(
    websocket: fastapi.WebSocket, phone_number: str, stream_id: str
):
    """Buffers incoming audio chunks and triggers processing on a pause."""
    try:
        # Initiate vad detector.
        vad_detector = voice_activity_detection.VoiceActivityDetection(
            rate=voice_assistant_constants.RATE,
            vad_frames_per_buffer=voice_assistant_constants.VAD_FRAMES_PER_BUFFER,
            bytes_per_sample=voice_assistant_constants.BYTES_PER_SAMPLE,
            idle_time_trigger_sec=voice_assistant_constants.IDLE_TIME_TRIGGER_SEC,
            chunk=voice_assistant_constants.CHUNK_LENGTH,
            vad_mode=voice_assistant_constants.VAD_MODE,
        )

        async for message in websocket.iter_text():
            if is_conversation_ended[phone_number]:
                return
            data = json.loads(message)

            # Handle mark tag received for last ai message sent.
            if data.get("event", None) == "mark":
                mark_tag = data["mark"]["name"]
                if mark_tag == "ai-message":
                    logging.info(f"Received mark event with name: {mark_tag}.")
                    is_ai_thinking[phone_number] = False
                    is_client_listening_to_ai[phone_number] = False

            # Skip incoming media events when ai is processing last audio chunk
            if is_ai_thinking[phone_number]:
                continue

            # Buffer incoming audio chunk and detect if speech is paused.
            if data.get("event", None) == "media":
                # Get audio chunk.
                raw_audio_bytes = (
                    audio_streaming_utils.convert_to_raw_audio_bytes(
                        ulaw_audio=data["media"]["payload"]
                    )
                )

                # Apply noise reduction.
                smooth_audio = audio_streaming_utils.reduce_noise_from_audio(
                    raw_audio_bytes=raw_audio_bytes
                )

                # Detect speaker activity
                speaker_state: SpeakerState = vad_detector.detect_activity(
                    audio_frame=smooth_audio, client_id=phone_number
                )

                if speaker_state == speaker_state.SPEAKING:
                    # Buffer incoming audio chunks when speaker is speaking.
                    client_audio_buffers[phone_number].append(smooth_audio)
                elif speaker_state == speaker_state.IDLE_FOR_A_WHILE:
                    # Trigger speech processing if speaker is idle
                    logging.info("Speaker is idle. Processing audio.")
                    is_ai_thinking[phone_number] = True
    except Exception as e:
        logging.error(f"Error while receiving audio from twilio : {e}")


async def handle_media_stream(
    websocket: fastapi.WebSocket,
    phone_number: str,
    stream_id: str,
    conversation_flow_handler: base_conversation_flow.BaseConversationFlow,
):
    """Handles bidirectional media stream."""
    await asyncio.gather(
        receive_from_twilio(
            websocket=websocket, phone_number=phone_number, stream_id=stream_id
        ),
        send_to_twilio(
            websocket=websocket,
            phone_number=phone_number,
            stream_id=stream_id,
            conversation_flow_handler=conversation_flow_handler,
        ),
        return_exceptions=True,
    )
