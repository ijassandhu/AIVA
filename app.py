from Brain import encode_image,analyze_img
from patient_voice import transcribed_with_groq
from doctor_voice import text_to_speech
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    print("PROCESS FUNCTION STARTED")
    print("Audio path:", audio_filepath)
    print("Image path:", image_filepath)
    
    if audio_filepath:
        speech_to_text_output = transcribed_with_groq(
            model="whisper-large-v3",
            filename=audio_filepath,
            GROQ_API_KEY=os.getenv("GROQ_API_KEY")
        )
    else:
        speech_to_text_output = "No audio provided"

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_img(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface with proper event handling
with gr.Blocks() as demo:
    gr.Markdown("# AI Doctor with Vision and Voice")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath",
                label="Record Your Voice"
            )
            image_input = gr.Image(
                type="filepath", 
                label="Upload Image (optional)"
            )
            submit_btn = gr.Button("Process", variant="primary")
        
        with gr.Column():
            speech_text = gr.Textbox(label="Speech to Text")
            doctor_response = gr.Textbox(label="Doctor's Response")
            audio_output = gr.Audio(
                label="Doctor's Voice Response",
                type="filepath",
                autoplay=True
            )

    # Set up event handlers
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_text, doctor_response, audio_output]
    )
demo.launch()