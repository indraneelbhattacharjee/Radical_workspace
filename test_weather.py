import vertexai
from vertexai.preview.generative_models import GenerativeModel, FunctionDeclaration, Tool, AutomaticFunctionCallingResponder
import speech_recognition as sr
import pyttsx3
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

# Initialize Vertex AI with project and location
vertexai.init(project="geminiexplorer-436616", location="us-central1")

# Initialize Open Meteo client 
om = openmeteo_requests.Client()

# Define a function that the model can use to answer questions about the weather
def get_current_weather(location: str, unit: str = "centigrade"):
    """Gets weather in the specified location using the Open Meteo API.

    Args:
        location: The location for which to get the weather.
        unit: Optional. Temperature unit. Can be Centigrade or Fahrenheit. Defaults to Centigrade.
    """
    # For simplicity, let's use Berlin's latitude and longitude
    latitude = 52.54
    longitude = 13.41

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
        "current": ["temperature_2m", "relative_humidity_2m"]
    }

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    # Extract current temperature and humidity
    current = response.Current()
    current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
    current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
    current_relative_humidity_2m = next(filter(lambda x: x.Variable() == Variable.relative_humidity and x.Altitude() == 2, current_variables))

    weather_info = {
        "location": f"Coordinates {response.Latitude()}°N {response.Longitude()}°E",
        "temperature": f"Current temperature: {current_temperature_2m.Value()}°C",
        "humidity": f"Current humidity: {current_relative_humidity_2m.Value()}%",
    }

    return weather_info

# Infer function schema
get_current_weather_func = FunctionDeclaration.from_func(get_current_weather)

# Tool is a collection of related functions
weather_tool = Tool(
    function_declarations=[get_current_weather_func],
)

# Use tools in chat with the model
model = GenerativeModel(
    "gemini-pro",
    tools=[weather_tool],
)

# Activate automatic function calling
afc_responder = AutomaticFunctionCallingResponder(
    max_automatic_function_calls=5,
)

# Start a chat session
chat = model.start_chat(responder=afc_responder)

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get voice input from the user
def get_voice_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=1)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            speak("There was an issue with the speech recognition service.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for speech.")
            speak("Listening timed out while waiting for speech.")
            return ""

# Main loop to interact with the AI via speech
def main():
    while True:
        # Get voice input from the user
        voice_command = get_voice_command()
        
        if voice_command:
            if "weather" in voice_command.lower():
                # Retrieve weather data using the Open Meteo API
                weather_data = get_current_weather("Berlin")  # Hardcoded to Berlin for demo purposes
                weather_report = f"{weather_data['location']}. {weather_data['temperature']}. {weather_data['humidity']}."
                print(weather_report)
                speak(weather_report)
            else:
                # Send the voice command to the model and get a response
                response = chat.send_message(voice_command)

                # Extract and print the model's response
                model_response = response.candidates[0].content.parts[0].text
                print(f"AI Response: {model_response}")

                # Speak the model's response out loud
                speak(model_response)
        
        # Option to break the loop if the user says "exit"
        if "exit" in voice_command.lower():
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
