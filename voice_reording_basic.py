import sounddevice as sd
from dotenv import load_dotenv
from scipy.io.wavfile import write
from datetime import datetime
import os

import assemblyai as aai
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


class VoiceApp():

    def __init__(self , duration=10 , fs=16000):
        self.duration = duration
        self.fs = fs
        self.filename = self._generate_filename()
        self.transcription_config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)


    def _generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"output_{timestamp}.wav"


    def record(self , duration=5 , filename="output.wav"):
        print(":studio_microphone: Recording...")
        audio = sd.rec(int(self.duration * self.fs) , samplerate=self.fs , channels=1)
        sd.wait()
        write(self.filename , self.fs , audio)
        print(f":white_check_mark: Saved as {self.filename}")


    def transcribe(self):
        print(":speech_balloon: Transcribing...")
        transcript = aai.Transcriber(config=self.transcription_config).transcribe(self.filename)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        self.transcript_text = transcript.text
        print(self.transcript_text)

        # Save transcript as a .txt file next to the .wav
        txt_filename = os.path.splitext(self.filename)[0] + ".txt"
        with open(txt_filename , "w" , encoding="utf-8") as f:
            f.write(self.transcript_text)

        print(f":page_facing_up: Transcript saved as {txt_filename}")


    """def transcribe():
        audio_file = "./output.wav"

        config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

        transcript = aai.Transcriber(config=config).transcribe(audio_file)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        print(transcript.text)"""

    """def transcribe(self):
        print(":speech_balloon: Transcribing...")
        transcript = aai.Transcriber(config=self.transcription_config).transcribe(self.filename)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        print(transcript.text)"""
