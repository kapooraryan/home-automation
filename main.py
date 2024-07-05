import streamlit as st
import pyaudio

from model_backend import interface
from web_backend.backend import *
from speech_to_text import Audio

model = interface.Model()

init_streamlit()

# Accept user input
if prompt := st.chat_input("What is up?"):
    add_user_message(prompt)
    add_model_message(model.infer(prompt))

# Audio input functionality
if st.button("Record Audio"):
    st.write("Recording audio...")

    # Audio recording using pyaudio
    chunk = 1024  # Record chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono audio
    fs = 16000  # Sampling rate (16KHz)
    seconds = 3  # Recording duration (seconds)

    try:
        # Initialize PyAudio object
        p = pyaudio.PyAudio()

        # Open audio stream
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        # Record audio data into a list
        recorded_frames = []
        for _ in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            recorded_frames.append(data)

        # # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()

        # Process the recorded audio (replace with your speech-to-text logic)
        # This example just shows converting the list to bytes
        recorded_audio_bytes = b''.join(recorded_frames)
        #print(recorded_audio_bytes)
        st.success("Recording finished! You can now process the audio data.")

        res = Audio.transcribe_audio(recorded_audio_bytes)

        # Speech to text function here
        # text = speech_to_text_function(recorded_audio_bytes)
        # st.write(f"Converted Text: hello")
        st.session_state.messages.append({"role": "user", "content": "test"})
        with st.chat_message("user"):
            st.write(res)
    except Exception as e:
        st.error(f"Error recording audio: {e}")
