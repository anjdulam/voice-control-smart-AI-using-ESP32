import speech_recognition as sr
import serial
import websocket
import time
import os
import json
import requests

recognizer=sr.Recognizer()
def process_text(text):
    res=requests.post("http://dgx.kmitonline.in:4000/",json={"input":text})
    if (res.json().get("output")=="0"):
        return "off"
    else:
        return "on"
def send_command_to_esp32(command):
    websocket_url = "ws://192.168.30.243:81"  # Replace with your ESP32 WebSocket server URL
    ws = websocket.create_connection(websocket_url)
    ws.send(command)
    ws.close()



def speech_to_text(recognizer, source, timeout=5):
    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)

    # Listen for audio input from the default microphone
    try:
        audio = recognizer.listen(source, timeout=timeout)
    except sr.WaitTimeoutError:
        print("Timeout occurred. No speech detected.")
        return None
    print("Processing...")
    try:
        # Use Google's speech recognition
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Request error:", e)
    return None
while True:
    print("Listening...")
    with sr.Microphone() as source:

        text = speech_to_text(recognizer, source)
        if text:
            print("You said:", text)
            if (process_text(text)=="on"):
                print("on") 
                send_command_to_esp32("on")
            else :
                print("off")
                send_command_to_esp32("off")

                                                                                                                                                                             