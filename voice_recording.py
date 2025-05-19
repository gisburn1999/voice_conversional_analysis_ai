import sounddevice as sd
from dotenv import load_dotenv
from scipy.io.wavfile import write
from datetime import datetime
import os
import assemblyai as aai
import numpy as np
import threading

from analyse_with_ai import Ai_Analyse

# Load API key from .env
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

class VoiceApp():
    def __init__(self, fs=44000, filename=None ):
        #self.duration = duration
        self.fs = fs
        self.filename = filename or self._generate_filename()
        #self.filename = self._generate_filename()
        self.recording = True
        self.audio = []
        self.transcription_config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.best,
            speaker_labels=True  #  Enables speaker diarization
        )
        self.transcript_text = None


    def _record_loop(self):
        print(":studio_microphone: Recording... Press ENTER to stop.")
        with sd.InputStream(samplerate=self.fs , channels=1 , callback=self._callback):
            input()  # Wait for user to press Enter
            self.recording = False


    def _callback(self , indata , frames , time , status):
        if self.recording:
            self.audio.append(indata.copy())


    def record(self):
        self.audio = []
        self.recording = True
        self._record_loop()

        audio_data = np.concatenate(self.audio , axis=0)
        folder = "recordings"
        os.makedirs(folder , exist_ok=True)
        filepath = os.path.join(folder , self.filename)
        write(filepath , self.fs , audio_data)
        print(f":white_check_mark: Saved as {self.filename} in folder {folder}")
        return filepath


    def _generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"output_{timestamp}.wav"


    def open_existing_file(self , filepath):
        try:
            with open(filepath , "r" , encoding="utf-8") as f:
                self.transcript_text = f.read()
            print("Transcript loaded successfully.")
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            self.transcript_text = None
        except Exception as e:
            print(f"Error loading file: {e}")
            self.transcript_text = None

    def transcribe(self , filepath=None):
        print(":: Transcribing...")

        # If no filepath is provided, use the default one
        if not filepath:
            filepath = os.path.join("recordings" , self.filename)

        # Transcribe using AssemblyAI
        transcript = aai.Transcriber(config=self.transcription_config).transcribe(filepath)

        if transcript.status == "error":
            raise RuntimeError(f"Transcription failed: {transcript.error}")

        # Process speaker-labeled transcript
        speaker_lines = []
        if transcript.utterances:
            for u in transcript.utterances:
                speaker = f"Speaker {u.speaker}"
                text = u.text.strip()
                speaker_lines.append(f"{speaker}: {text}")
        else:
            speaker_lines.append("No speaker-labeled utterances found.")

        self.transcript_text = "\n".join(speaker_lines)
        print("Preview (first 3 lines):")
        print("\n".join(self.transcript_text.splitlines()[:3]))

        # Save to text file
        os.makedirs("transcripts" , exist_ok=True)
        txt_filename = os.path.splitext(self.filename)[0] + ".txt"
        txt_filepath = os.path.join("transcripts" , txt_filename)

        with open(txt_filepath , "w" , encoding="utf-8") as f:
            f.write(self.transcript_text)

        print(f":page_facing_up: Transcript saved as {txt_filename}")
        return txt_filepath

    def print_recording(self):
        if self.transcript_text == None:
            print("Nothing to show, do a recording first")
        else:
            print(f"Here is the full transcript of the last recording:\n{self.transcript_text}")


    def run_ai_analysis(self):
        if self.transcript_text:
            ai_app = Ai_Analyse(self.transcript_text)
            ai_app.speaker_analysis()
        else:
            print("No transcript available. Please transcribe or load a file first.")


    def analys_claude(self):
        if self.transcript_text:
            ai_app = Ai_Analyse(self.transcript_text)
            ai_app.problem_analysis()
        else:
            print("No transcript available. Please transcribe or load a file first.")


    def analyse_groq(self):
        if self.transcript_text:
            ai_app = Ai_Analyse(self.transcript_text)
            ai_app.basic_groq_analysing()
        else:
            print("No transcript available. Please transcribe or load a file first.")
