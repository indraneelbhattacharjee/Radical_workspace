import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession, SafetySetting

# Streamlit app title
st.title("Sparks!")

# Initialize Streamlit session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Vertex AI with your project and location
vertexai.init(project="geminiexplorer-436616", location="us-central1")

# Define the generation configuration
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Define safety settings
safety_settings = [
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
]

# Try to load the Gemini model
model = None
try:
    model = GenerativeModel("gemini-1.5-flash-002")
except Exception as e:
    st.error(f"Model loading failed: {e}")

# Function to send query to the model
def llm_function(model: GenerativeModel, query):
    try:
        if model:
            responses = model.generate_content(
                [query],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True
            )
            output = ""
            for response in responses:
                output += response.text
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": output})
        else:
            st.error("Model is not initialized.")
    except Exception as e:
        st.error(f"Error in content generation: {e}")

# Capture user name
user_name = st.text_input("What's your name?")

# Check if message history is empty, send personalized initial message
if len(st.session_state.messages) == 0 and user_name:
    initial_prompt = f"Hello {user_name}! I’m ReX, your assistant powered by Google Gemini! 🎉 How can I assist you today?"
    llm_function(model, initial_prompt)

# Display previous messages
for message in st.session_state.messages:
    try:
        st.chat_message(message['role']).markdown(message['content'])
    except AttributeError:
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Get user input
query = st.chat_input("Ask about Gemini Flights!")

# Process the query only if the model is initialized
if query:
    st.chat_message("user").markdown(query)
    llm_function(model, query)

    # Display the assistant's response
    if st.session_state.messages:
        response = st.session_state.messages[-1]['content']
        st.chat_message("assistant").markdown(response)
    else:
        st.error("No messages in the session state.")
