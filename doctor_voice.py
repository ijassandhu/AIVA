import os 
from gtts import gTTS
import subprocess
import platform
from pydub.playback import play
from pydub import AudioSegment

def text_to_speech(input_text, output_filepath):
    language = "en"

    audio_obj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audio_obj.save(output_filepath)
    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])

        elif os_name == "Windows":
            audio = AudioSegment.from_file(output_filepath)
            play(audio)

        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'

        else:
            raise OSError("Unsupported operating system")

    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
    
    return output_filepath

