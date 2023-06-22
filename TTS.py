import os
import time
from gtts import gTTS
from pydub.playback import play
from pygame import mixer

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp.mp3"
    tts.save(filename)

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    while mixer.music.get_busy(): 
            time.sleep(0.01)
    
    mixer.music.unload()    
    os.remove(filename) 