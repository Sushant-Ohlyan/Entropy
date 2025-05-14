import pyaudio

# Audio configuration
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1  # Mono audio
SAMPLE_RATE = 44100  # 44.1 kHz sample rate (CD-quality audio)
BUFFER_SIZE = 1024  # Number of frames per buffer

# Create an instance of PyAudio
pyaudio_instance = pyaudio.PyAudio()

def record_audio():
    """
    Records a chunk of audio from the microphone.
    
    Returns:
        bytes: A chunk of audio data.
    """
    try:
        # Open the audio stream for recording
        audio_stream = pyaudio_instance.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS,
                                             rate=SAMPLE_RATE, input=True,
                                             frames_per_buffer=BUFFER_SIZE)
        
        # Record audio for the specified chunk size
        audio_data = audio_stream.read(BUFFER_SIZE)
        
        # Close the stream after recording
        audio_stream.stop_stream()
        audio_stream.close()
        
        return audio_data
    
    except Exception as e:
        print(f"Error occurred while recording audio: {e}")
        return None
