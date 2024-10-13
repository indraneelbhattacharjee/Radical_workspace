# Voice-Activated Weather Assistant

This project is a voice-activated assistant that fetches real-time weather data using the Open Meteo API and interacts with users through voice commands. The assistant also integrates with Vertex AI to provide conversational responses for general queries. The system listens for commands, processes them, fetches weather information, and responds with text-to-speech output.

## Features

- **Real-Time Weather**: Uses the Open Meteo API to fetch current weather data such as temperature and humidity.
- **Voice Command Input**: Users can issue commands via voice, which are processed using Google's Speech Recognition API.
- **Voice Output**: The assistant responds to users' queries with spoken responses via `pyttsx3`.
- **Conversational AI**: Integrates with Vertex AI's generative models for general conversation.

## Requirements

Ensure that the following dependencies are installed before running the project.

### Dependencies

The project requires the following Python packages:

```bash
google-cloud-aiplatform
SpeechRecognition
pyaudio (or sounddevice as an alternative)
pyttsx3
openmeteo-requests
```

### Install Instructions

To install all required packages, run the following command:

#### Using `pyaudio`:

```bash
pip install google-cloud-aiplatform SpeechRecognition pyaudio pyttsx3 openmeteo-requests
```

#### Using `sounddevice` (if you encounter issues with `pyaudio`):

```bash
pip install google-cloud-aiplatform SpeechRecognition sounddevice pyttsx3 openmeteo-requests
```

## Setup

### 1. Vertex AI Setup

1. Create a Vertex AI project in Google Cloud and get the project ID.
2. Ensure your `gcloud` SDK is authenticated to the right project:
   ```bash
   gcloud auth application-default login
   gcloud config set project [YOUR_PROJECT_ID]
   ```
3. Update the project and location values in the code:
   ```python
   vertexai.init(project="your-project-id", location="us-central1")
   ```

### 2. Open Meteo API

- The Open Meteo API is free to use and doesn't require an API key.
- The project is pre-configured to fetch weather data for Berlin. You can modify the `latitude` and `longitude` values to get weather for other locations.

## Running the Project

1. Clone this repository and navigate to the project folder.
2. Install the required dependencies (see above).
3. Run the Python script:
   ```bash
   python test_weather.py
   ```

## How It Works

1. The system listens for voice commands. If the command includes the word "weather," it fetches real-time weather data.
2. If the user asks a general question or makes a non-weather-related command, it sends the query to the Vertex AI generative model.
3. The system responds to the user with voice output for both weather and non-weather queries.

## Example

- **Command**: "What is the weather like?"
- **Response**: "Coordinates 52.54°N 13.41°E. Current temperature: 22°C. Current humidity: 50%."

- **Command**: "Tell me a joke."
- **Response**: "Sure! Here's a joke from Vertex AI..."

## Known Issues

- If `pyaudio` fails to install, use `sounddevice` as an alternative for microphone input.
- Ensure that the microphone permissions are enabled for your system if speech recognition isn't working.

## Contributing

Feel free to open issues or contribute to the project through pull requests. Any improvements, bug fixes, or new feature suggestions are welcome!

## License

This project is open-source and licensed under the MIT License.

# gemini-explorer
