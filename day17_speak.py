import os
from gtts import gTTS
import pygame
import time

# 1. The Message
# In a real app, this would come from your AI Agent or a system check.
text_to_speak = "Hi Trent. I'm not going to talk dirty to you, but I am going to alert you that your server CPU temperature is too high. Please check the cooling system."

# 2. Generate Audio (The "Mouth")
# We use Google's TTS API (free via this wrapper)
print(f"--- GENERATING AUDIO: '{text_to_speak}' ---")
tts = gTTS(text=text_to_speak, lang='en', slow=False)

# Save to your new data folder so git ignores it
audio_file = "data/alert.mp3" 
tts.save(audio_file)
print(f"Audio saved to {audio_file}")

# 3. Play Audio (The "Speaker")
# We use pygame mixer to play it directly in the script
pygame.mixer.init()
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# Keep script running while audio plays
print("--- PLAYING AUDIO ---")
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("--- DONE ---")