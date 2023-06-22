import os
import time, io
import openai
import sys, shutil
from SpeechRecognition import SpeechRecognizer
from chatGPT import chatGPT
from gtts import gTTS
from pydub.playback import play
from pygame import mixer
import textwrap
import bcolors as b

# Configuration of the openAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SR = SpeechRecognizer()


def print_conversation(conversation):
    os.system('cls' if os.name == 'nt' else 'clear')  # cls pour Windows, clear pour Unix
    system_msg, user_msg, assistant_msg = "", "", ""

    for item in conversation:
        if item['role'] == 'system':
            system_msg = item['content']
        elif item['role'] == 'user':
            user_msg = item['content']
        elif item['role'] == 'assistant':
            assistant_msg = item['content']

    term_size = shutil.get_terminal_size()
    term_width = term_size.columns
    adjusted_width = int(term_width * 0.8)  # Utiliser 80% de la largeur du terminal
    half_width = adjusted_width // 2 - 3  # -3 for padding and '|'

    def print_line(msg, width):
        lines = textwrap.wrap(msg, width)
        for line in lines:
            print(b.OK +"| " + line + " " * (width - len(line)) + " |"+ b.END)
        return len(lines)

    print(b.OK +"+" + "-" * (adjusted_width - 2) + "+"+ b.END)
    print(b.OK + "| SYSTEM MESSAGE: "+ b.END)
    print_line(system_msg, adjusted_width - 4)  # -4 pour tenir compte des espaces de marge et du symbole '|'
    print(b.OK + "+" + "-" * (adjusted_width - 2) + "+" + b.END)

    user_lines = textwrap.wrap(user_msg, half_width)
    assistant_lines = textwrap.wrap(assistant_msg, half_width)
    max_lines = max(len(user_lines), len(assistant_lines))

    # Print user and assistant messages side by side
    for i in range(max_lines):
        user_line = user_lines[i] if i < len(user_lines) else ""
        assistant_line = assistant_lines[i] if i < len(assistant_lines) else ""
        print(b.BLUE + "| " + user_line.ljust(half_width) + b.ENDC + "| "+ b.WARN + assistant_line.ljust(half_width) + " |" + b.ENDC)

    print("+" + "-" * (adjusted_width - 2) + "+")

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