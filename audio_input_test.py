import sounddevice as sd
import numpy as np

fs = 44100
duration = 3  # seconds

print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float32')
sd.wait()
print("Done.")

print("Min:", np.min(recording))
print("Max:", np.max(recording))
print("Mean:", np.mean(recording))
print("First 10 samples:", recording[:10].flatten())
