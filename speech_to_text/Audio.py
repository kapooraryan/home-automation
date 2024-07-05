import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

# Load the model outside the function for better performance
audio_model = whisper.load_model("medium.en")  # Load the whisper model

def transcribe_audio(audio_data):
  print("Function has been called")
  audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
  result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
  print(result)
  text = result['text'].strip()
  return text