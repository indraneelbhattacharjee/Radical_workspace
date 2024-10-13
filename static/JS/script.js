let recognition;
const chatBox = document.getElementById("chat-box");

// Initialize Speech Recognition
if (!('webkitSpeechRecognition' in window)) {
    alert('Web Speech API is not supported by this browser. Upgrade to a newer version of Chrome.');
} else {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = function (event) {
        const userInput = event.results[0][0].transcript;
        displayMessage(userInput, 'user-message');
        askJarvis(userInput); // Send to Jarvis via voice input
    };

    recognition.onerror = function (event) {
        displayMessage('Error occurred in recognition: ' + event.error, 'jarvis-message');
    };
}

// Start speech recognition
function startRecognition() {
    if (recognition) {
        recognition.start();
    } else {
        console.error("Speech recognition not supported.");
    }
}

// Check if the form and elements exist before adding event listener
const jarvisForm = document.getElementById("jarvis-form");
const userInputField = document.getElementById("user-input");

if (jarvisForm && userInputField) {
    jarvisForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const userInput = userInputField.value.trim();
        if (userInput) {
            userInputField.value = ""; // Clear input field
            displayMessage(userInput, 'user-message');
            askJarvis(userInput); // Send to Jarvis via text input
        }
    });
} else {
    console.error("Form or input field not found.");
}

// Display message in chat box
function displayMessage(message, className) {
    if (chatBox) {
        const messageElement = document.createElement('div');
        messageElement.className = className;
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    } else {
        console.error("Chat box element not found.");
    }
}

// Send user input (either text or voice) to the backend with error handling
// Send user input (either text or voice) to the backend with error handling
async function askJarvis(userInput) {
    try {
        const response = await fetch('http://127.0.0.1:5000/ask-jarvis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput }),
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response from Jarvis:", data); // Debugging: log the response

        if (data.reply) {
            displayMessage(data.reply, 'jarvis-message');

            // Call the text-to-speech function to speak Jarvis' response
            speakResponse(data.reply);
        } else {
            displayMessage('No reply from Jarvis.', 'jarvis-message');
        }
    } catch (error) {
        console.error('Error:', error); // Log the error for debugging
        displayMessage('Sorry, something went wrong while contacting Jarvis.', 'jarvis-message');
    }
}


// Text-to-Speech (TTS) using Web Speech API
function speakResponse(text) {
    if ('speechSynthesis' in window) {
        const speech = new SpeechSynthesisUtterance();
        speech.text = text;
        speech.lang = 'en-US';
        speech.volume = 1;
        speech.rate = 1;
        speech.pitch = 1;
        window.speechSynthesis.speak(speech);
    } else {
        console.error("Text-to-speech not supported.");
    }
}
