import pyttsx3

def text_to_speech(text):
    # initialize Text-to-speech engine
    engine = pyttsx3.init()

    # convert text to speech
    engine.say(text)
                             
    # play the speech
    engine.runAndWait()

if __name__ == "__main__":
    # Get text input from the user
    text_input = input("Enter the text you want to convert to speech: ")

    # Convert text to speech
    text_to_speech(text_input)
