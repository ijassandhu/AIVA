import logging
import speech_recognition as sr
from groq import Groq
from pydub import AudioSegment
from dotenv import load_dotenv
from io import BytesIO
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

def record_audio(file_path , timeout = 20 , phrase_time_limit = None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str) : Path to save the recorded audio file.
    timeout (int) : Maximum time for the phrase to start(in seconds).
    phrase_time_limit (int) : Maximum time for the phrase to be recorded (in seconds).
    """

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now....")

            audio_data = recognizer.listen(source,timeout=timeout,phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format='mp3', bitrate = "128k")

            logging.info(f'Audio saved to {file_path}')

    except Exception as e:
        logging.error(f'An error occured:{e}')

def transcribed_with_groq(model,filename,GROQ_API_KEY):
    client = Groq(api_key = GROQ_API_KEY)
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model=model,
        temperature=0,
        response_format="verbose_json",
        )
        return transcription.text
        