import os
import openai
import sys
from SpeechRecognition import SpeechRecognizer
from chatGPT import chatGPT
from pydub.playback import play

from TermUI import print_conversation
from TTS import text_to_speech

# Configuration of the openAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SR = SpeechRecognizer()

if __name__=="__main__":
    if len(sys.argv) >= 2:
        agent_chosen=sys.argv[1]
        lang = sys.argv[2]
    else:
        agent_chosen = None
        lang = "en"

    chatbot = chatGPT(agent=agent_chosen, language=lang)
    conv = [{"role": "system", "content": chatbot.agent_data["PrePrompt"]}]
    os.system('cls' if os.name == 'nt' else 'clear')  # cls pour Windows, clear pour Unix
    while True:
        text = SR.interpret()
        conv = chatbot.thinkAbout(text, conv)
        print_conversation(conv)
        # The text that you want to convert to audio
        mytext = conv[-1]["content"]
        
        text_to_speech(mytext, lang=lang)