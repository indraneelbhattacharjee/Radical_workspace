from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import vertexai
from vertexai.generative_models import GenerativeModel
import os

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# Load API key from environment
Jarvis = os.getenv('JARVIS_KEY_OPENAI')

# Initialize Vertex AI with your project settings
vertexai.init(project="geminiexplorer-436616", location="us-central1")

# Create generative model instance
model = GenerativeModel("gemini-1.5-flash-002")

# Configuration for the model
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Route for rendering the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling user input
@app.route('/ask-jarvis', methods=['POST'])
def ask_jarvis():
    try:
        # Get the JSON data from the request
        user_input = request.json.get('message')

        # If no message is provided, return an error
        if not user_input:
            return jsonify({"error": "Invalid input, message required"}), 400

        # Log the received message for debugging
        print(f"Received input: {user_input}")

        # Start a chat with the generative model
        chat = model.start_chat()

        # Generate a response based on the user input
        response = chat.send_message(user_input, generation_config=generation_config)

        # Log the generated response for debugging
        print(f"Generated response: {response.text}")

        # Return the generated response in JSON format
        return jsonify({"reply": response.text})

    except Exception as e:
        # Log the error message for debugging
        print(f"Error occurred: {e}")
        return jsonify({"error": "Something went wrong. Please try again later."}), 500

# Starting the Flask app
if __name__ == '__main__':
    app.run(debug=True)
