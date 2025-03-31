import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import requests
from datetime import datetime
import math

# Download required NLTK data (run this once)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")
    print("Please ensure you have an internet connection and try again.")
    exit(1)

# Chatbot name
CHATBOT_NAME = "Aash"

# OpenWeather API key (your provided key)
WEATHER_API_KEY = "b02f2b1fcf150005eee65f2d0301cc97"
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Predefined responses for the chatbot
GREETINGS = ["hello", "hi", "hey", "greetings"]
GREETING_RESPONSES = [f"Hi there! I'm {CHATBOT_NAME}.", f"Hello! I'm {CHATBOT_NAME}, nice to meet you!", f"Hey! I'm {CHATBOT_NAME}!"]
FAREWELL = ["bye", "goodbye", "see you"]
FAREWELL_RESPONSES = ["Goodbye! Have a great day!", "See you later!", "Bye bye!"]
HOW_ARE_YOU = ["how are you", "how you doing", "how's it going"]
HOW_ARE_YOU_RESPONSES = ["I'm doing great, thanks for asking!", "I'm good, how about you?", "Doing awesome, thanks!"]
NAME_QUESTIONS = ["what is your name", "who are you", "what's your name"]
WEATHER_QUESTIONS = ["weather", "temperature", "forecast"]
TIME_QUESTIONS = ["time", "what time is it", "current time"]
DEFAULT_RESPONSES = [
    "That's interesting! Tell me more.",
    "I see, what else can we talk about?",
    "Cool! What’s on your mind?",
    "Hmm, I’m not sure about that, but let’s keep chatting!"
]

# Expanded knowledge base
KNOWLEDGE_BASE = {
    "capital of france": "The capital of France is Paris.",
    "capital of germany": "The capital of Germany is Berlin.",
    "capital of japan": "The capital of Japan is Tokyo.",
    "capital of india": "The capital of India is New Delhi.",
    "capital of brazil": "The capital of Brazil is Brasília.",
    "capital of australia": "The capital of Australia is Canberra.",
    "capital of canada": "The capital of Canada is Ottawa.",
    "capital of united states": "The capital of the United States is Washington, D.C.",
    "capital of united kingdom": "The capital of the United Kingdom is London.",
    "capital of south africa": "The capital of South Africa is Pretoria (administrative), Cape Town (legislative), and Bloemfontein (judicial).",
    "president of the united states": "As of March 2025, the President of the United States is Donald Trump. He was sworn in as the 47th president on January 20, 2025.",
    "president of france": "As of March 2025, the President of France is Emmanuel Macron. He has been in office since May 14, 2017.",
    "president of brazil": "As of March 2025, the President of Brazil is Luiz Inácio Lula da Silva, commonly known as Lula. He was sworn in on January 1, 2023.",
    "president of india": "As of March 2025, the President of India is Droupadi Murmu. She was sworn in on July 25, 2022.",
    "president of south africa": "As of March 2025, the President of South Africa is Cyril Ramaphosa. He has been in office since February 15, 2018.",
    "largest planet": "The largest planet in our solar system is Jupiter.",
    "boiling point of water": "The boiling point of water is 100 degrees Celsius at standard pressure."
}

# Function to preprocess user input
def preprocess_text(text):
    try:
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation.replace('+', '').replace('-', '').replace('*', '').replace('/', '')))
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        return tokens, text
    except Exception as e:
        return [], text

# Function to preprocess for calculations
def preprocess_for_calculation(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation.replace('+', '').replace('-', '').replace('*', '').replace('/', '')))
    return text

# Function to convert worded numbers and operators
def convert_words_to_expression(text):
    number_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }
    operator_words = {
        "plus": "+", "minus": "-", "times": "*", "divided by": "/", "divide": "/"
    }
    
    for word, digit in number_words.items():
        text = text.replace(word, digit)
    for word, symbol in operator_words.items():
        text = text.replace(word, symbol)
    return text

def extract_math_expression(text):
    text = text.lower()

    if "square root of" in text:
        num = text.split("square root of")[-1].strip()
        if num.replace('.', '', 1).isdigit():
            return f"sqrt {num}"

    if "cube root of" in text:
        num = text.split("cube root of")[-1].strip()
        if num.replace('.', '', 1).isdigit():
            return f"cbrt {num}"

    if "power" in text:
        parts = text.split(" power ")
        if len(parts) == 2 and parts[0].strip().replace('.', '', 1).isdigit() and parts[1].strip().replace('.', '', 1).isdigit():
            return f"{parts[0].strip()} ^ {parts[1].strip()}"

    return None

# Function to perform calculations
def calculate(expression):
    try:
        parts = expression.split()
        if len(parts) != 3:
            return "Please provide a simple calculation in the form 'number operator number' (e.g., 2 + 3)."
        
        num1, operator, num2 = parts
        num1 = float(num1)
        num2 = float(num2)

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Division by zero is not allowed."
            result = num1 / num2
        else:
            return "Invalid operator. Please use +, -, *, or /."
        
        return f"The result of {expression} is {result}."
    except Exception as e:
        return f"Error in calculation: {e}"

# Function to extract mathematical expressions
def extract_math_expression(text):
    calc_text = preprocess_for_calculation(text)
    converted_text = convert_words_to_expression(calc_text)
    words = converted_text.split()
    for i in range(len(words) - 2):
        if (words[i].replace('.', '', 1).lstrip('-').isdigit() and 
            words[i + 1] in ['+', '-', '*', '/'] and 
            words[i + 2].replace('.', '', 1).lstrip('-').isdigit()):
            return f"{words[i]} {words[i + 1]} {words[i + 2]}"
    return None



# Function to get current time
def get_current_time():
    current_time = datetime.now().strftime("%H:%M:%S on %B %d, %Y")
    return f"The current time is {current_time} (local system time)."

# Function to get weather
def get_weather(city):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    
    try:
        response = requests.get(WEATHER_BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is currently {description} with a temperature of {temp}°C."
        elif response.status_code == 401:
            return "Error: Invalid API key. Please check your OpenWeather API key."
        elif response.status_code == 404:
            return f"Sorry, I couldn't find weather data for {city}. Please check the city name."
        else:
            return f"Error: Received status code {response.status_code}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: Network issue - {e}"
    except ValueError as e:
        return f"Error parsing weather data: {e}"

# Function to extract city from weather query
def extract_city(raw_text):
    words = raw_text.split()
    if "in" in words:
        in_index = words.index("in")
        if in_index + 1 < len(words):
            return words[in_index + 1]
    return None

NEWS_API_KEY = "f264f387739e41d6a6ca71e0797a4cac"
NEWS_BASE_URL = "https://newsapi.org/v2/top-headlines"

# Function to fetch news
def get_news(country="us", category=None):
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
    }
    if category:
        params["category"] = category
    
    try:
        response = requests.get(NEWS_BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            articles = data.get("articles", [])
            if articles:
                top_news = random.choice(articles)
                return f"Here’s some news: {top_news['title']} - {top_news['url']}"
            return "Sorry, I couldn’t find any news at the moment."
        return f"Error fetching news: {data.get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"
    
# Function to check knowledge base
def check_knowledge_base(raw_text):
    for question, answer in KNOWLEDGE_BASE.items():
        if question in raw_text:
            return answer
    return None

def get_person_info(person):
    wikipedia_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{person.replace(' ', '_')}"
    
    try:
        response = requests.get(wikipedia_url)
        data = response.json()
        
        if response.status_code == 200 and "extract" in data:
            return data["extract"]
        return f"Sorry, I couldn't find information about {person}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"


# Function to get response
def get_response(user_input):
    tokens, raw_text = preprocess_text(user_input)

    if not tokens and not raw_text:
        return "Sorry, I had trouble understanding that. Can you try again?"

    # Check for greetings
    if any(word in tokens for word in GREETINGS):
        return random.choice(GREETING_RESPONSES)
    
    # Check for farewells
    if any(word in tokens for word in FAREWELL):
        return random.choice(FAREWELL_RESPONSES)
    
    # Check for "how are you"
    if any(phrase in raw_text for phrase in HOW_ARE_YOU):
        return random.choice(HOW_ARE_YOU_RESPONSES)
    
    if "who is" in raw_text or "tell me about" in raw_text:
        person = raw_text.replace("who is ", "").replace("tell me about ", "").strip()
        return get_person_info(person)

    # Check for name questions
    if any(phrase in raw_text for phrase in NAME_QUESTIONS):
        return f"My name is {CHATBOT_NAME}! Nice to meet you!"
    
    # Check for time questions
    if any(phrase in raw_text for phrase in TIME_QUESTIONS):
        return get_current_time()
    
    if "news" in raw_text:
        return get_news()
    
    # Check for weather questions
    if any(word in tokens for word in WEATHER_QUESTIONS):
        city = extract_city(raw_text)
        if city:
            return get_weather(city)
        return "Please specify a city (e.g., 'weather in London')."
    
    # Check for calculations
    if "calculate" in raw_text or "what is" in raw_text:
        expression = extract_math_expression(user_input)
        if expression:
            return calculate(expression)
    
    # Check knowledge base
    knowledge_response = check_knowledge_base(raw_text)
    if knowledge_response:
        return knowledge_response
    
    # Default response
    return random.choice(DEFAULT_RESPONSES)

# Main chatbot loop
def chatbot():
    print(f"Chatbot: Hi! I'm {CHATBOT_NAME}, your friendly chatbot. I can tell you the time, weather, and more! (Type 'bye' to exit)")
    
    while True:
        try:
            user_input = input("You: ")
            if not user_input.strip():
                print("Chatbot: Please say something! I’m here to help.")
                continue
            if "bye" in user_input.lower():
                print("Chatbot:", random.choice(FAREWELL_RESPONSES))
                break
            
            response = get_response(user_input)
            print("Chatbot:", response)
        except KeyboardInterrupt:
            print("\nChatbot: Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"Chatbot: Oops, something went wrong: {e}. Let’s try again!")

if __name__ == "__main__":
    chatbot()