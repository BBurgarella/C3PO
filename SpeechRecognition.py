import speech_recognition as sr
import os
import openai

class SpeechRecognizer:

    def __init__(self):
        # Create a recognizer object
        self.r = sr.Recognizer()

    def interpret(self):
        # Start the microphone
        with sr.Microphone() as source:
            print("Say Anything :")
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_whisper_api(audio, api_key=openai.api_key)
                print("You said : {}".format(text))
                return text 
            except:
                print("Sorry could not recognize what you said")