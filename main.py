#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
import pyaudio
import wave
import speech_recognition as sr
from selenium.webdriver.common.by import By
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#Set up whisper API for speech recognition
r = sr.Recognizer()

# Set up Visual ChatGPT for context analysis
visual_chatgpt = pipeline("text2text-generation", model="microsoft/DialoGPT-medium", device=0)

# Set the recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("Recording...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop recording and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio to a file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Load the audio file
audio_file = sr.AudioFile("output.wav")

# Transcribe the audio
with audio_file as source:
    audio = r.record(source)

# Recognize speech using Google Speech Recognition
try:
    text = r.recognize_google(audio)
    print("Transcription: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

################################

# Identify user's intent from text
if "Open Chrome and make a tweet about" in text:
    task = "tweet"
elif "Open Chrome and search for" in text:
    task = "search"
else:
    task = "not defined"

# Use Visual ChatGPT for context analysis
context = visual_chatgpt(text, max_length=50, num_return_sequences=1)

# Execute task based on user's intent and context analysis
if task == "tweet":
    # Code to open Chrome and navigate to Twitter
    # Populate the tweet with the text provided by the user
    username = "ENTER_YOUR_USERNAME"
    password = "ENTER_YOUR_PASSWORD"

    tweet = text.split("Open Chrome and make a tweet about")[1]

    driver = webdriver.Chrome('chromedriver')
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(5)
    driver.find_element(by='name', value='text').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
    time.sleep(5)
    if password == "":
        print('Enter a password')
    driver.find_element(by='name', value='password').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@role='textbox']").send_keys(tweet)
    time.sleep(3)
    driver.find_element(By.XPATH, '//div[@data-testid="toolBar"]/div[2]/div[3]/div').click()
    time.sleep(2)
    print("Tweet posted successfully!")
elif task == "search":
    # Code to open Chrome and search for the query provided by the user
    # set the path to your Chrome driver executable file
    chromedriver_path = '/path/to/chromedriver'

    # create a new instance of Chrome driver
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    query = text.split("Open Chrome and search for")[1]

    # navigate to Google search page
    driver.get('https://www.google.com')

    # find the search box element and enter the query
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # close the browser
    driver.quit()
    print("Search completed successfully!")
else:
    print("Unknown task. Please try again.")

# Respond to the user
# You can use any text-to-speech technology here
response = "Your task has been completed successfully!"
print(response)
