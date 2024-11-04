"""Cusp Money AI voice assistant server to handle incoming twilio calls.

Sample command:

python -m app_voice_assistant
"""

import asyncio
import logging

import fastapi
import uvicorn
from fastapi import responses
from twilio.twiml import voice_response

from constants import voice_assistant_constants
from utils import data_utils, google_docs_utils, onboarding_utils
from utils.speech_processing import audio_streaming_utils
from voice_assistant_modules import (
    default_audio_responses,
    handle_human_ai_conversation,
)
from voice_assistant_modules.conversation_flows import (
    advice_explanation,
    advisor_questionnaire,
)

UserJourneyStage = onboarding_utils.UserJourneyStage

app = fastapi.FastAPI()


@app.get("/", response_class=responses.JSONResponse)
async def index_page():
    """Default response to check if service is live or not."""
    return {"message": "Cusp AI media server is running !"}


@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: fastapi.Request):
    """Handle incoming call and return TwiML response to connect to audio."""
    response = voice_response.VoiceResponse()

    # Get phone number from incoming call.
    form_data = await request.form()
    phone_number = form_data.get("Caller")
    phone_number = (
        phone_number.replace("+91", "").replace("-", "").replace(" ", "")
    )
    logging.info(f"Incoming call from {phone_number}.")

    # Send TwiML response to start websocket connection to receive and send
    # audio.
    host = request.url.hostname
    connect = voice_response.Connect()
    connect.stream(url=f"wss://{host}/media-stream/{phone_number}")
    response.append(connect)
    return responses.HTMLResponse(
        content=str(response), media_type="application/xml"
    )


@app.websocket("/media-stream/{phone_number}")
async def handle_incoming_audio_stream(
    websocket: fastapi.WebSocket, phone_number: str
):
    """Handles incoming audio chunks received from caller's end."""
    try:
        await websocket.accept()
        logging.info(f"Websocket connection established with {phone_number}.")

        # Check user's state in onboarding journey.
        user_journey_state: UserJourneyStage = (
            onboarding_utils.detect_user_journey_state(
                phone_number=phone_number
            )
        )
        logging.info(f"Current state of user is : {user_journey_state.name}")

        # Get the stream id and set in state
        stream_id = await audio_streaming_utils.get_stream_id(
            websocket=websocket
        )

        # Handle different user journey stages.
        match user_journey_state:
            # Notify user to complete onboarding and share accounts data
            # through account aggregator and end the call.
            case UserJourneyStage.AA_DATA_PENDING:
                await default_audio_responses.send_text_as_audio(
                    input_text=voice_assistant_constants.NOTIFY_ONBOARDING_PENDING,
                    websocket=websocket,
                    stream_sid=stream_id,
                    target_language_code=voice_assistant_constants.DEFAULT_AI_LANGUAGE,
                )
                await asyncio.sleep(1)
                await websocket.close()  # Hang the call

            # Start a 1:1 conversation with user to get answers for advisor's
            # questionnaire.
            case UserJourneyStage.CUSTOMER_PROFILE_PENDING:
                # Start conversation by conveying the agenda.
                await default_audio_responses.send_text_as_audio(
                    input_text=voice_assistant_constants.NOTIFY_AGENDA_OF_QUESTIONNAIRE,
                    websocket=websocket,
                    stream_sid=stream_id,
                    target_language_code=voice_assistant_constants.DEFAULT_AI_LANGUAGE,
                )
                # Load list of questions
                questionnaire = data_utils.load_json_from_disk(
                    filepath=voice_assistant_constants.ADVISOR_QUESTIONNAIRE_PATH
                )
                # Initiate llm based conversation handler
                creds, docs_service, drive_service = (
                    google_docs_utils.get_google_doc_creds()
                )
                doc_id = data_utils.get_doc_by_phone(phone_number=phone_number)
                doc_content = google_docs_utils.get_doc_as_md(
                    doc_id=doc_id, drive_service=drive_service
                )
                conversation_flow_handler = (
                    advisor_questionnaire.AdvisorQuestionnaireConversation(
                        questionnaire=questionnaire,
                        aa_summary=doc_content,
                    )
                )
                conversation_flow_handler.add_ai_message(
                    text=voice_assistant_constants.NOTIFY_AGENDA_OF_QUESTIONNAIRE
                )
                # Continue conversation until all the answered are not provided
                await handle_human_ai_conversation.handle_media_stream(
                    websocket=websocket,
                    phone_number=phone_number,
                    stream_id=stream_id,
                    conversation_flow_handler=conversation_flow_handler,
                )
                # Save the human response summary to google doc.
                if conversation_flow_handler.is_conversation_ended():
                    conversation_flow_handler.save_answer_to_doc(
                        doc_id=doc_id, creds=creds, docs_service=docs_service
                    )
                await asyncio.sleep(5)
                await websocket.close()  # Hang the call

            # Suggest user that advisor has not completed advise generation
            case UserJourneyStage.ADVICE_GENERATION_PENDING:
                await default_audio_responses.send_text_as_audio(
                    input_text=voice_assistant_constants.NOTIFY_ADVICE_PENDING,
                    websocket=websocket,
                    stream_sid=stream_id,
                    target_language_code=voice_assistant_constants.DEFAULT_AI_LANGUAGE,
                )
                await asyncio.sleep(5)
                await websocket.close()  # Hang the call

            # Describe the advice first and then solve user's doubts regarding
            # human advisor's notes.
            case UserJourneyStage.ADVICE_EXISTS:
                await default_audio_responses.send_text_as_audio(
                    input_text=voice_assistant_constants.NOTIFY_AGENDA_OF_QA_OVER_ADVICE,
                    websocket=websocket,
                    stream_sid=stream_id,
                    target_language_code=voice_assistant_constants.DEFAULT_AI_LANGUAGE,
                )
                # Initiate llm based conversation handler
                _, _, drive_service = google_docs_utils.get_google_doc_creds()
                doc_id = data_utils.get_doc_by_phone(phone_number=phone_number)
                doc_content = google_docs_utils.get_doc_as_md(
                    doc_id=doc_id, drive_service=drive_service
                )
                conversation_flow_handler = (
                    advice_explanation.AdviceExplanationConversation(
                        customer_profile_and_advice=doc_content
                    )
                )
                conversation_flow_handler.add_ai_message(
                    text=voice_assistant_constants.NOTIFY_AGENDA_OF_QA_OVER_ADVICE
                )
                # Continue conversation until all the answered are not provided
                await handle_human_ai_conversation.handle_media_stream(
                    websocket=websocket,
                    phone_number=phone_number,
                    stream_id=stream_id,
                    conversation_flow_handler=conversation_flow_handler,
                )
                await asyncio.sleep(5)  # Wait for last message to finish.
                await websocket.close()  # Hang the call
    except fastapi.WebSocketDisconnect:
        logging.error("Websocket connection closed by caller.")
        return
    except Exception as e:
        logging.error(f"Error in handle incoming audio stream {e}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=voice_assistant_constants.PORT)
