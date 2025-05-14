from flask import Flask, Response, render_template
import pyaudio

app = Flask(__name__)

# Audio configuration
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 2
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024

# Initialize PyAudio instance
audio = pyaudio.PyAudio()

def generate_wav_header(sample_rate, bits_per_sample, channels):
    """
    Generates a WAV header based on the provided audio settings.
    """
    data_size = 2000 * 10**6  # Placeholder data size
    header = bytes("RIFF", 'ascii') 
    header += (data_size + 36).to_bytes(4, 'little')  
    header += bytes("WAVE", 'ascii')  
    header += bytes("fmt ", 'ascii')  
    header += (16).to_bytes(4, 'little')  
    header += (1).to_bytes(2, 'little')  
    header += (channels).to_bytes(2, 'little')  
    header += (sample_rate).to_bytes(4, 'little')  
    header += (sample_rate * channels * bits_per_sample // 8).to_bytes(4, 'little')  
    header += (channels * bits_per_sample // 8).to_bytes(2, 'little')  
    header += (bits_per_sample).to_bytes(2, 'little')  
    header += bytes("data", 'ascii')  
    header += (data_size).to_bytes(4, 'little')  
    return header

@app.route('/audio')
def audio_stream():
    """
    Streams live audio from the microphone to the client.
    """
    def generate_audio_stream():
        wav_header = generate_wav_header(SAMPLE_RATE, 16, CHANNELS)

        # Open audio stream for recording
        stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS,
                            rate=SAMPLE_RATE, input=True,
                            input_device_index=1, frames_per_buffer=CHUNK_SIZE)
        
        print("Recording started...")

        first_run = True
        while True:
            if first_run:
                audio_data = wav_header + stream.read(CHUNK_SIZE)
                first_run = False
            else:
                audio_data = stream.read(CHUNK_SIZE)
            yield audio_data

    return Response(generate_audio_stream())

@app.route('/')
def home():
    """
    Renders the home page for audio streaming.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
