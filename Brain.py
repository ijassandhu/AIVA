import os
import base64
from groq import Groq 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# image_path = "images/rashes-care-at-patient-care.webp"


def encode_image(image_path):
    image_file = open(image_path, 'rb')
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image



# query = "Is there something wrong with my skin?"

# model="meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_img(query, model,encoded_image):
  client = Groq()
  completion = client.chat.completions.create(
      model = model,
      messages=[
        {
          "role": "user",
          "content": [{
                      "type" : "text",
                      "text": query
                      },
          {
          "type":"image_url",
          "image_url":{"url":f"data:image/jpeg;base64,{encoded_image}"}
          }]
        }
      ],
      temperature=1,
      max_completion_tokens=1024,
      top_p=1,
      stream=True,
      stop=None
  )
  response_content = ""
  for chunk in completion:
      if chunk.choices[0].delta.content:
          response_content += chunk.choices[0].delta.content
  return response_content
