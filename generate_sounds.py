import wave
import math
import struct
import os

def generate_tone(filename, frequency=440, duration=0.5, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Simple sine wave
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

def generate_slide_tone(filename, start_freq=440, end_freq=880, duration=0.5, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Linear frequency slide
            freq = start_freq + (end_freq - start_freq) * (i / n_samples)
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

output_dir = 'static/sounds'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Happy: Rising tone (C5 to E5 roughly)
generate_slide_tone(os.path.join(output_dir, 'happy.wav'), start_freq=523, end_freq=659, duration=0.4)

# Sad: Falling tone
generate_slide_tone(os.path.join(output_dir, 'sad.wav'), start_freq=440, end_freq=220, duration=0.6)

# Angry: Low rumble (low frequency)
generate_tone(os.path.join(output_dir, 'angry.wav'), frequency=100, duration=0.5)

# Surprise: Sharp rising high tone
generate_slide_tone(os.path.join(output_dir, 'surprise.wav'), start_freq=800, end_freq=1500, duration=0.3)

# Neutral: Steady mid tone
generate_tone(os.path.join(output_dir, 'neutral.wav'), frequency=440, duration=0.2)

print("Sounds generated in static/sounds/")
