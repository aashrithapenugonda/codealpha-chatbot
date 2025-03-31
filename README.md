```markdown
# Aash Chatbot

This is a Python-based chatbot named "Aash" that can perform various tasks such as providing the current time, weather information, news updates, basic calculations, and answering general knowledge questions.

## Features

-   **Greetings and Farewells:** Handles basic greetings and farewells.
-   **Time Information:** Provides the current time.
-   **Weather Information:** Fetches and displays weather data for a specified city.
-   **News Updates:** Retrieves and displays top news headlines.
-   **Basic Calculations:** Performs simple arithmetic calculations.
-   **General Knowledge:** Answers questions based on a predefined knowledge base.
-   **Person Information:** Retrieves information about people from Wikipedia.
-   **Error Handling:** Robust error handling for network requests and input processing.

## Prerequisites

-   Python 3.x
-   `nltk` library
-   `requests` library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2.  **Install dependencies:**
    ```bash
    pip install nltk requests
    ```

3.  **Download NLTK data:**
    Run the script once to download the required NLTK data.
    ```bash
    python chatbot.py
    ```
    The script will automatically download the necessary NLTK packages (`punkt` and `stopwords`).

4.  **Obtain API Keys:**
    -   You need an OpenWeather API key to fetch weather data. Replace `"b02f2b1fcf150005eee65f2d0301cc97"` with your actual API key in the `chatbot.py` file.
    -   You need a News API key to fetch news data. Replace `"f264f387739e41d6a6ca71e0797a4cac"` with your actual API key in the `chatbot.py` file.
    -   Sign up for free API keys on the OpenWeather and News API websites.

## Usage

1.  **Run the chatbot:**
    ```bash
    python chatbot.py
    ```

2.  **Interact with the chatbot:**
    Type your questions or commands in the console.

3.  **Example interactions:**
    -   "Hi"
    -   "What time is it?"
    -   "Weather in London"
    -   "Calculate 2 + 3"
    -   "What is the capital of France?"
    -   "Who is Albert Einstein?"
    -   "Bye"

## Code Structure

-   `chatbot.py`: Contains the main chatbot logic and functions.

## Dependencies

-   `nltk`: Natural Language Toolkit for text processing.
-   `requests`: For making HTTP requests to fetch weather and news data.

## API Keys

-   OpenWeather API key: For weather information.
-   News API key: For news updates.

## Notes

-   The chatbot uses a predefined knowledge base for general questions. You can expand this knowledge base by adding more question-answer pairs to the `KNOWLEDGE_BASE` dictionary.
-   Ensure you have a stable internet connection for weather and news updates.
-   The chatbot handles basic arithmetic calculations. For more complex calculations, you may need to extend the `calculate` function.

## Author

[P.Aashritha Mounika]
