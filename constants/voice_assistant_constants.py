"""Constants used by Voice assistant module."""

import pyaudio

# Server
PORT = 5050

# Input and output audio stream configuration.
CHUNK_LENGTH = 160  # Read this many chunks at a time from input source
FORMAT = pyaudio.paInt16  # Raw audio format
BYTES_PER_SAMPLE = 2
CHANNELS = 1
RATE = 8000  # Hz

# Voice activity config
VAD_FRAMES_PER_BUFFER = int(RATE * 0.03)  # Detect speech for given audio chunk
IDLE_TIME_TRIGGER_SEC = 0.5  # Max pause to trigger speech processing
VAD_MODE = 3  # Refer https://docs.rs/webrtc-vad/latest/src/webrtc_vad/lib.rs.html#125-133


# Sarvam API (Speech processing)
SARVAM_BASE_URL = "https://api.sarvam.ai/"
DEFAULT_AI_LANGUAGE = "hi-IN"
SARVAM_API_KEY = ""
SPEECH_PROCESSING_MIN_BYTES = 1000  # Minimum bytes for processing speech
RECORDINGS_DIR = "data/recordings"


# Conversation flows config
ADVISOR_QUESTIONNAIRE_PATH = "data/voice_assistant/advisor_questionnaire.json"


# Default responses
NOTIFY_ONBOARDING_PENDING = (
    "Hello! Welcome to Cusp Money. Here, you receive financial advice"
    "from a registered investment advisor. To get started, please first"
    "share your account data through an RBI-registered account"
    "aggregator. For this, go to hackathon.cusp.money to provide consent"
    "for data sharing. After that, you can call us again. Thank you!"
)
NOTIFY_AGENDA_OF_QUESTIONNAIRE = (
    "Welcome to Cusp Money! Thank you for sharing your account aggregator "
    "data. This call is crucial as it "
    "allows us to understand your unique financial goals and "
    "circumstances, ensuring our advice is truly personalized. Today, "
    "I'll ask a few questions to tailor our guidance to your specific "
    "situation. Should we start?"
)

NOTIFY_ADVICE_PENDING = (
    "Sorry, we apologize for the inconvenience. At the moment, our "
    "financial advisor has no available financial advice for you. "
    "Please call back after some time. Thank you, and have a good day."
)


NOTIFY_AGENDA_OF_QA_OVER_ADVICE = (
    "Thank you for your patience. Our registered financial advisor has "
    "reviewed your account summary and analyzed the answers to additional "
    "questions. We are pleased to inform you that your advice is ready "
    "now. Would you like a brief overview first, or do you already "
    "have some questions in mind?"
)
