import speech_recognition as sr

def recognize_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()

    audio = None
    with mic as source:
        audio = r.listen(source)

    return r.recognize_google(audio)

def infer(message: str) -> str:
    return message

result = infer(recognize_speech())
print(result)
