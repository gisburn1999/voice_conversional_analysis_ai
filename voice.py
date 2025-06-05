import assemblyai as aai

aai.settings.api_key = "4ec36919b8884d7682363b12044cd633"


#with open("output.wav", "rb") as sound:
audio_file = "recordings/output.wav"



config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)