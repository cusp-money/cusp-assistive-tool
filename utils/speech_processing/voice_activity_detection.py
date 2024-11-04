"""Helper library for voice activity detection based on webrtc-vad."""

import enum

import webrtcvad


class SpeakerState(enum.Enum):
    """State of speaker."""

    SPEAKING = 1
    NOT_SPEAKING = 2
    IDLE_FOR_A_WHILE = 3


class VoiceActivityDetection:
    """Voice activity detection such as speaking or idle."""

    def __init__(
        self,
        rate: int,
        vad_frames_per_buffer: int,
        bytes_per_sample: int,
        idle_time_trigger_sec: int,
        chunk: int,
        vad_mode: int = 3,
    ) -> None:
        """Initialise the state of VAD instance."""
        self.sample_rate = rate
        self.frame_size = vad_frames_per_buffer
        self.bytes_per_sample = bytes_per_sample
        self.idle_cut = int(idle_time_trigger_sec / (chunk / rate))
        self.last_voice_activity = {}
        self.vad = webrtcvad.Vad(mode=vad_mode)

    def detect_activity(self, audio_frame, client_id) -> SpeakerState:
        """Detects if speaker is speaking or idle for a while."""
        last_30_ms = audio_frame[-self.frame_size * self.bytes_per_sample :]
        idle_time = self._manage_client_idle(client_id)
        converted_frame = self._convert_buffer_size(last_30_ms)
        is_speech = self.vad.is_speech(
            converted_frame, sample_rate=self.sample_rate
        )
        if is_speech:
            self.last_voice_activity[client_id] = 0
            return SpeakerState.SPEAKING
        else:
            if idle_time == self.idle_cut:
                self.last_voice_activity[client_id] = 0
                return SpeakerState.IDLE_FOR_A_WHILE
            else:
                self.last_voice_activity[client_id] += 1
                return SpeakerState.NOT_SPEAKING

    def _convert_buffer_size(self, audio_frame: bytes) -> bytes:
        """Pads audio chunk to max length."""
        while len(audio_frame) < (self.frame_size * self.bytes_per_sample):
            audio_frame = audio_frame + b"\x00"
        return audio_frame

    def _manage_client_idle(self, client_id: str) -> int:
        """Manages the state of being idle for given client."""
        if client_id not in self.last_voice_activity:
            self.last_voice_activity[client_id] = 0
        return self.last_voice_activity[client_id]
