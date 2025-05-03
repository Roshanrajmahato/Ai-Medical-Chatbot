import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key=os.environ.get("GROQ_API_KEY")

image_path="acne.jpg"
image_file=open(image_path,"rb")
encoded_image=base64.b64encode(image_file.read()).decode('utf-8')

client=Groq(api_key=groq_api_key) 
query="Is there something wrong with my face?" 
model="meta-llama/llama-4-scout-17b-16e-instruct"
messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]

chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

print(chat_completion.choices[0].message.content)