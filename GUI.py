from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


import os
import openai
from SpeechRecognition import SpeechRecognizer
from chatGPT import chatGPT
from pydub.playback import play
from TTS import text_to_speech

# Configuration of the openAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SR = SpeechRecognizer()


class MainApp(App):


    def build(self):
        # Main Layout
        self.agent = "C3PO"
        self.lang = "en"
        self.chatbot = chatGPT(agent=self.agent, language=self.lang)
        self.conv = [{"role": "system", "content": self.chatbot.agent_data["PrePrompt"]}]
        # Main Layout
        main_layout = BoxLayout(orientation="vertical")

        # Create the dropdown
        Menubar_layout = BoxLayout(orientation="horizontal", height=40,size_hint_y=0.2)
        dropdown = DropDown()
        lang_drop = DropDown()

        # Add buttons (options) to the dropdown

        files = os.listdir("agents")

        for file in files:
            if ".json" in file:
                btn = Button(text=file[:-5], size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn=btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)
        # Create the main button
        main_button = Button(text='Choose an agent', size_hint=(None, None), height=44, width=150)

        self.languages = {'Afrikaans': 'af', 'Arabic': 'ar', 'Bulgarian': 'bg', 'Bengali': 'bn', 'Bosnian': 'bs', 'Catalan': 'ca', 'Czech': 'cs', 'Danish': 'da', 'German': 'de', 'Greek': 'el', 'English': 'en', 'Spanish': 'es', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Gujarati': 'gu', 'Hindi': 'hi', 'Croatian': 'hr', 'Hungarian': 'hu', 'Indonesian': 'id', 'Icelandic': 'is', 'Italian': 'it', 'Hebrew': 'iw', 'Japanese': 'ja', 'Javanese': 'jw', 'Khmer': 'km', 'Kannada': 'kn', 'Korean': 'ko', 'Latin': 'la', 'Latvian': 'lv', 'Malayalam': 'ml', 'Marathi': 'mr', 'Malay': 'ms', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Dutch': 'nl', 'Norwegian': 'no', 'Polish': 'pl', 'Portuguese': 'pt', 'Romanian': 'ro', 'Russian': 'ru', 'Sinhala': 'si', 'Slovak': 'sk', 'Albanian': 'sq', 'Serbian': 'sr', 'Sundanese': 'su', 'Swedish': 'sv', 'Swahili': 'sw', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Filipino': 'tl', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Vietnamese': 'vi', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Mandarin/Taiwan)': 'zh-TW', 'Chinese (Mandarin)': 'zh'}
        for language, key in self.languages.items():
            btn = Button(text=language, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn=btn: lang_drop.select(btn.text))
            lang_drop.add_widget(btn)


        # Create the main button
        main_button_lang = Button(text='Choose a language', size_hint=(None, None), height=44, width=150)

        # Show the dropdown menu when the main button is released
        # Note: all the bind() calls pass the instance of the caller (here, the button),
        # as the first argument of the callback (here, the function).
        main_button.bind(on_release=dropdown.open)
        main_button_lang.bind(on_release=lang_drop.open)

        # Assign the data to the button text and close the dropdown when a button is selected
        dropdown.bind(on_select=self.set_agent)
        lang_drop.bind(on_select=self.set_lang)

        Menubar_layout.add_widget(main_button)
        Menubar_layout.add_widget(main_button_lang)
        main_layout.add_widget(Menubar_layout)

        # System Label and Text Field
        system_label = Label(text="System", size_hint_y=None, height=20)
        self.system_field = TextInput(readonly=True)
        self.system_field._set_text(self.chatbot.agent_data["PrePrompt"])
        main_layout.add_widget(system_label)
        main_layout.add_widget(self.system_field)

        # User and Assistant Label and Text Field in one row
        row_layout = BoxLayout(orientation="horizontal")
        user_layout = BoxLayout(orientation="vertical")
        assistant_layout = BoxLayout(orientation="vertical")

        user_label = Label(text="User", size_hint_y=None, height=20)
        self.user_field = TextInput(readonly=True)
        user_layout.add_widget(user_label)
        user_layout.add_widget(self.user_field)

        assistant_label = Label(text="Assistant", size_hint_y=None, height=20)
        self.assistant_field = TextInput(readonly=True)
        assistant_layout.add_widget(assistant_label)
        assistant_layout.add_widget(self.assistant_field)

        row_layout.add_widget(user_layout)
        row_layout.add_widget(assistant_layout)
        main_layout.add_widget(row_layout)

        # Editable Text Field
        message_input = TextInput(multiline=False, size_hint=(1, None), height=50)

        # Submit and Speak Buttons
        button_layout = BoxLayout(size_hint=(1, None), height=50, orientation="horizontal")
        submit_button = Button(text="Submit")
        speak_button = Button(text="Speak")
        speak_button.bind(on_press=self.speak_message)
        button_layout.add_widget(message_input)
        button_layout.add_widget(submit_button)
        button_layout.add_widget(speak_button)
        main_layout.add_widget(button_layout)

        return main_layout

    def set_agent(self, instance, agent):
        self.agent = agent
        self.chatbot = chatGPT(agent=agent, language=self.languages[self.lang])
        self.conv = [{"role": "system", "content": self.chatbot.agent_data["PrePrompt"]}]
        self.system_field._set_text(self.chatbot.agent_data["PrePrompt"])

    def set_lang(self, instance, lang):
        self.lang = lang
        self.chatbot = chatGPT(agent=self.agent, language=self.languages[lang])
        self.conv = [{"role": "system", "content": self.chatbot.agent_data["PrePrompt"]}]
        self.system_field._set_text(self.chatbot.agent_data["PrePrompt"])

    def set_item(self, instance, value):
        self.menu.caller.text = value
        self.menu.dismiss()

    def send_message(self, event):
        message = self.message_input.text
        self.message_input.text = ""
        self.messageManager(message, speak=False)

    def speak_message(self, event):
        # Insert the function that activates SpeechRecognition here
        text = SR.interpret()
        self.messageManager(text, speak=True)
        
    def messageManager(self, message, speak=True):
        self.user_field.text += f"> {message}\n"
        self.conv = self.chatbot.thinkAbout(message, self.conv)
        # The text that you want to convert to audio
        self.assistant_field.text += f"> {self.conv[-1]['content']}\n"
        text_to_speech(self.conv[-1]['content'], lang=self.languages[self.lang])

if __name__ == "__main__":
    MainApp().run()
