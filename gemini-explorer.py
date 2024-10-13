import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

st.title("Gemini Flights!")

# Initialize Streamlit session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Vertex AI
vertexai.init(project="geminiexplorer-436616", location="us-central1")  # Set your project and location

# Try to load the "text-bison" model
model = None
chat = None

try:
    model = GenerativeModel(model_name="text-bison")
    chat = ChatSession(model=model)
except Exception as e:
    st.error(f"Model loading failed: {e}")

# Function to send query to the model
def llm_function(chat: ChatSession, query):
    try:
        if chat:
            response = chat.send_message(query)
            output = response.text
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": output})
        else:
            st.error("Chat session is not initialized.")
    except Exception as e:
        if "429" in str(e):
            st.error("Quota exceeded. Please wait or request a quota increase from Google Cloud.")
        else:
            st.error(f"Error in chat session: {e}")

# Capture user name
user_name = st.text_input("What's your name?")

# Check if message history is empty, send personalized initial message
if len(st.session_state.messages) == 0 and user_name:
    initial_prompt = f"Hello {user_name}! I’m ReX, your assistant powered by Google Gemini! 🎉 How can I assist you today?"
    llm_function(chat, initial_prompt)

# Display previous messages
for message in st.session_state.messages:
    try:
        st.chat_message(message['role']).markdown(message['content'])
    except AttributeError:
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Get user input
query = st.chat_input("Ask about Gemini Flights!")

# Process the query only if chat session is initialized
if query:
    st.chat_message("user").markdown(query)
    llm_function(chat, query)

    # Display the assistant's response
    if st.session_state.messages:
        response = st.session_state.messages[-1]['content']
        st.chat_message("assistant").markdown(response)
    else:
        st.error("No messages in the session state.")
