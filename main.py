import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import win32com.client
import speech_recognition as sr
import os
import datetime

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def Speak(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=44100) as source:
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Bunny"

def send_message():
    message = entry.get()
    if message:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "You: " + message + "\n")
        chatbox.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        process_command(message)

def process_command(command):
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"],
             ["google", "https://www.google.com"]]
    for site in sites:
        if f"Open {site[0]}".lower() in command.lower():
            speaker.Speak(f"Opening {site[0]}...")
            webbrowser.open(site[1])
        if "the time" in command:
            strfTime = datetime.datetime.now().strftime("%H hours: %M minutes : %S seconds")
            speaker.Speak(f"Sir, the time is {strfTime}")

def start_voice_recording():
    Speak("Hello, I am Bunny AI.")
    while True:
        print("Listening...")
        query = takeCommand()
        if query.lower() == "stop":
            Speak("Goodbye!")
            break
        process_command(query)

root = tk.Tk()
root.title("Chatbox with Send Button and Mic")

# Set background color for the main window
root.configure(bg="lightpink")

# Create a scrolled text widget to display the chat
chatbox = scrolledtext.ScrolledText(root, state=tk.DISABLED, bg="lightblue")
chatbox.pack(fill=tk.BOTH, expand=True)

# Create an entry widget for typing messages
entry = tk.Entry(root, bg="white")
entry.pack(fill=tk.BOTH, expand=True)

# Create a Frame for the send button, microphone button, and clear chat button
button_frame = tk.Frame(root, bg="darkgrey")
button_frame.pack(fill=tk.X)

# Create a "Send" button to send messages
send_button = tk.Button(button_frame, bg="lightpink", text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=5)

# Create a "Mic" button for starting voice recording
mic_button = tk.Button(button_frame, bg="lightpink", text="Mic", command=start_voice_recording)
mic_button.pack(side=tk.LEFT, padx=10, pady=5)

# Create a "Clear Chat" button to clear the chatbox
clear_button = tk.Button(button_frame, bg="lightpink", text="Clear Chat", command=lambda: chatbox.delete(1.0, tk.END))
clear_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Start the main event loop
root.mainloop()

