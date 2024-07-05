from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import sounddevice as sd

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load processor, model, vocoder, and embeddings dataset
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

def text_to_speech(text):
    # Preprocess text
    inputs = processor(text=text, return_tensors="pt").to(device)
    # Get Indian male speaker embeddings
    speaker_embeddings = torch.tensor(embeddings_dataset[4535]["xvector"]).unsqueeze(0).to(device)
    # Generate speech with the models
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    # Convert speech tensor to numpy array
    speech_np = speech.cpu().numpy()
    # Play the speech audio
    sd.play(speech_np, samplerate=16000)
    sd.wait()

if __name__ == "__main__":
    text_input = input("Enter the text you want to convert to speech: ")
    text_to_speech(text_input)
