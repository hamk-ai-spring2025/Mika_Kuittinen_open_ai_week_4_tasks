import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import os
from deep_translator import GoogleTranslator

def interpreter_program():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        start_time = time.time()
        audio = recognizer.listen(source)
        print("Recognizing...")

        try:
            # Speech to Text
            text = recognizer.recognize_google(audio)
            print(f"Transcribed Text: {text}")
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return

        # Translate Text
        target_language = 'es'  # Change this if you want a different language (e.g., 'es' = Spanish)
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        print(f"Translated Text: {translated_text}")

        # Text to Speech
        tts = gTTS(translated_text, lang=target_language)
        filename = "translated_audio.mp3"
        tts.save(filename)

        # Play audio using pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Ensure resources are released properly
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Measure Delay
        end_time = time.time()
        delay = end_time - start_time
        print(f"Total Delay: {delay:.2f} seconds")

        # Remove audio file
        os.remove(filename)

if __name__ == "__main__":
    interpreter_program()
