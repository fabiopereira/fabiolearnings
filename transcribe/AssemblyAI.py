# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "MY KEY"
transcriber = aai.Transcriber()

# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
transcript = transcriber.transcribe("/Users/fabiopereira/Downloads/papai/PAP3_01.mp3")

print(transcript.text)