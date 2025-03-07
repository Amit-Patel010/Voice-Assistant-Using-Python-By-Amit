import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
import datetime
import os
import webbrowser
import wikipedia
import smtplib
import pyjokes
import requests
import json

recognizer = sr.Recognizer()
speaker = pyttsx3.init()

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return None

def execute_task(command):
    if 'play' in command and 'on youtube' in command:
        song = command.replace('play', '').replace('on youtube', '').strip()
        speak(f"Playing {song} on YouTube.")
        kit.playonyt(song)

    elif 'open' in command and 'website' in command:
        website = command.replace('open', '').replace('website', '').strip()
        speak(f"Opening {website}.")
        webbrowser.open(f"http://{website}")

    elif 'what time' in command:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"The current time is {time}.")

    elif 'search' in command and 'wikipedia' in command:
        query = command.replace('search', '').replace('wikipedia', '').strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"Here's what I found on Wikipedia: {result}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results, please be more specific.")
        except wikipedia.exceptions.HTTPTimeoutError:
            speak("Sorry, I couldn't fetch information from Wikipedia right now.")

    elif 'open' in command:
        application = command.replace('open', '').strip()
        speak(f"Opening {application}.")
        try:
            os.system(f"start {application}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {application}. Error: {str(e)}")

    elif 'tell me a joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'send an email' in command:
        speak("What should the subject be?")
        subject = listen()
        speak("What should the email body contain?")
        body = listen()
        speak("Please provide the recipient's email address.")
        recipient_email = listen()

        try:
            send_email(subject, body, recipient_email)
            speak("Email sent successfully!")
        except Exception as e:
            speak(f"Sorry, I couldn't send the email. Error: {str(e)}")

    elif 'convert currency' in command:
        speak("Please provide the amount and the currency to convert from (e.g., 100 USD to EUR).")
        conversion_input = listen()
        convert_currency(conversion_input)

    elif 'what is' in command:
        query = command.replace('what is', '').strip()
        try:
            result = wikipedia.summary(query, sentences=1)
            speak(f"Here's what I found: {result}")
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results. Be more specific.")
        except Exception as e:
            speak(f"Sorry, I couldn't find that information. Error: {str(e)}")

    elif 'quit' in command or 'exit' in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I don't know how to perform that task.")

def send_email(subject, body, recipient_email):
    sender_email = "your_email@example.com"  
    sender_password = "your_password"  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(sender_email, recipient_email, message)
    server.quit()

def convert_currency(conversion_input):
    try:
        amount, from_currency, _, to_currency = conversion_input.split()
        amount = float(amount)

        api_key = "your_api_key"
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"

        response = requests.get(url)
        data = response.json()

        from_rate = data['rates'].get(from_currency.upper())
        to_rate = data['rates'].get(to_currency.upper())

        if from_rate and to_rate:
            conversion_rate = to_rate / from_rate
            converted_amount = amount * conversion_rate
            speak(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
        else:
            speak("Sorry, I couldn't retrieve the conversion rates. Please check the currencies and try again.")
    except Exception as e:
        speak(f"Sorry, I couldn't process the conversion. Error: {str(e)}")

def run_assistant():
    speak("Hello, I am your customizable voice assistant. How can I assist you today?")
    
    while True:
        command = listen()
        
        if command:
            execute_task(command)

if __name__ == "__main__":
    run_assistant()
