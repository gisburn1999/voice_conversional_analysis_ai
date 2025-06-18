import assemblyai as aai
from dotenv import load_dotenv
import os
load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


#with open("output.wav", "rb") as sound:
audio_file = "recordings/output.wav"



config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)