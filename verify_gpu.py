import tensorflow as tf
import sys

print(f"TensorFlow Version: {tf.__version__}")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPUs Detected: {len(gpus)}")
    for gpu in gpus:
        print(f"  - {gpu}")
else:
    print("No GPUs detected. TensorFlow is running on CPU.")

sys.exit(0 if gpus else 1)
