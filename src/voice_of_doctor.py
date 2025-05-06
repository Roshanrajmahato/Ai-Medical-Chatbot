# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


# input_text="Hi this is Ai with Hassan!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs



def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice
# its not working properly used second one 
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['start', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# input_text="Hi this is Ai with Roshan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


# Anothre way from ChatGPT
# used it
from gtts import gTTS
from playsound import playsound
import platform
import os

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    # Convert text to speech and save as mp3
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    try:
        os_name = platform.system()
        if os_name in ["Windows", "Darwin", "Linux"]:
            playsound(output_filepath)
        else:
            raise OSError(f"Unsupported operating system: {os_name}")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")

# Example usage
# input_text = "Hi this is AI with Hassan, autoplay testing!"
# output_file = "gtts_testing_autoplay.mp3"
# text_to_speech_with_gtts(input_text=input_text, output_filepath=output_file)

from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        os_name = platform.system()
        if os_name in ["Windows", "Darwin", "Linux"]:
            playsound(output_filepath)
        else:
            raise OSError(f"Unsupported operating system: {os_name}")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")
# input_text="Hi this is Ai with Roshan, autoplay testing!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")