import sounddevice as sd
import numpy as np

# Step 1: List available input devices
print("\nAvailable input devices:")
devices = sd.query_devices()
input_devices = [(i, dev) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]

for i, dev in input_devices:
    print(f"{i}: {dev['name']} - {dev['max_input_channels']} channels")

# Step 2: Choose device
device_index = int(input("\nEnter the number of the input device you want to use: "))
channels = int(input("Enter number of channels to use (usually 1 or 2): "))

# Step 3: Record a few seconds
duration = 5  # seconds
samplerate = 44100

print("\nRecording...")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='float32', device=device_index)
sd.wait()
print("Recording complete.")

# Step 4: Playback
print("Playing back...")
sd.play(recording, samplerate)
sd.wait()
print("Done.")
