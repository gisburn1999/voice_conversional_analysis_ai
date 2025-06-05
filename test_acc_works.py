from pydub import AudioSegment
test = AudioSegment.silent(duration=1000)
test.export("test.aac", format="aac")

