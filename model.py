import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import os

Jarvis = os.getenv('JARVIS_KEY_OPENAI')

def multiturn_generate_content():
    vertexai.init(project="geminiexplorer-436616", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    chat = model.start_chat()
    while True:


        print(chat.send_message((input("Ask Jarvis!")),
        generation_config=generation_config,
        #safety_settings=safety_settings
        ))
    pass


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

'''safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]'''

multiturn_generate_content()
