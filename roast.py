import os
import speech_recognition as sr
import openai
from gtts import gTTS
import pygame
import time

# Hae OpenAI API key ympäristömuuttujasta
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tarkista että API-avain löytyy
if not openai.api_key:
    raise ValueError("OpenAI API key not found! Make sure OPENAI_API_KEY environment variable is set.")

def listen_to_microphone(prompt_text="Speak now..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt_text)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")
            return None

def voice_controlled_roaster():
    print("🎙️ Welcome to the Voice Roaster!")
    print("👉 Say the roast style you want: 'funny', 'brutal', 'sarcastic', or 'positive'.")

    style = listen_to_microphone("Please say the roast style now...")
    if style is None:
        print("⚠️ No style detected, defaulting to 'funny'.")
        style = "funny"

    if "brutal" in style:
        roast_style = "Make a brutal roast."
    elif "sarcastic" in style:
        roast_style = "Make a sarcastic roast."
    elif "positive" in style:
        roast_style = "Make a positive and light-hearted roast."
    else:
        roast_style = "Make a funny roast."

    print("🎯 Now, say the topic to roast...")

    topic = listen_to_microphone("Please say the topic now...")
    if topic is None:
        print("⚠️ No topic detected, using 'life' as default.")
        topic = "life"

    print(f"🧠 Generating a {style} roast about {topic}...")

    try:
        start_time = time.time()
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a professional comedian. {roast_style}"},
                {"role": "user", "content": f"Roast {topic}."}
            ]
        )
        roast = response.choices[0].message.content
        print(f"\n🎤 Generated Roast:\n{roast}\n")
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return

    # Teksti puheeksi
    tts = gTTS(roast, lang='en')
    filename = "roast_audio.mp3"
    tts.save(filename)

    # Toistetaan ääni pygame:lla
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Suljetaan ja vapautetaan resurssit
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    end_time = time.time()
    delay = end_time - start_time
    print(f"⏱️ Total Delay: {delay:.2f} seconds")

    # Poistetaan väliaikainen tiedosto
    #os.remove(filename)

if __name__ == "__main__":
    voice_controlled_roaster()
