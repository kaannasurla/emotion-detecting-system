from flask import Flask, Response, jsonify, request, render_template
from flask_cors import CORS
import cv2
import numpy as np
from emotion_detector_mediapipe import EmotionDetector as MediapipeDetector
from emotion_detector_tensorflow import EmotionDetector as TensorflowDetector
import json
import random
import os
from datetime import datetime
import base64
from collections import deque, Counter

app = Flask(__name__)
CORS(app)  # Activează CORS

# Inițializare detectori
detectors = {}

# 1. Mediapipe (Default)
try:
    detectors['mediapipe'] = MediapipeDetector()
    print("✅ Mediapipe detector initialized")
except Exception as e:
    print(f"❌ Failed to initialize Mediapipe: {e}")

# 2. Tensorflow (Old AI)
try:
    tf_detector = TensorflowDetector()
    if tf_detector.model_loaded:
        detectors['tensorflow'] = tf_detector
        print("✅ Tensorflow detector initialized")
    else:
        print("⚠️ Tensorflow model could not be loaded. Restricted to Mediapipe only.")
except Exception as e:
    print(f"❌ Failed to initialize Tensorflow detector: {e}")

# Setare model curent default
current_model_name = 'mediapipe' if 'mediapipe' in detectors else list(detectors.keys())[0] if detectors else None

def get_current_detector():
    if not current_model_name or current_model_name not in detectors:
        # Fallback
        if 'mediapipe' in detectors:
            return detectors['mediapipe']
        elif detectors:
            return list(detectors.values())[0]
        else:
            raise Exception("No detectors available")
    return detectors[current_model_name]

# Configurare categorii emoji
EMOJI_CATEGORIES = {
    'happy': ['😊', '😄', '🤗', '😁', '🥳', '😍', '🌟'],
    'sad': ['😢', '😔', '😞', '😿', '💔', '😭', '☹️'],
    'angry': ['😠', '😡', '🤬', '👿', '💢', '😤', '💥'],
    'surprise': ['😲', '😮', '🤯', '😳', '🎊', '✨', '🎉'],
    'neutral': ['😐', '😑', '🙂', '😶', '😏', '🤔', '😌']
}

# Culori pentru bounding box (format HEX pentru CSS/Canvas)
EMOTION_COLORS = {
    'happy': '#00ff00',      # Verde
    'sad': '#0000ff',        # Albastru
    'angry': '#ff0000',      # Roșu
    'surprise': '#ffff00',   # Galben
    'neutral': '#808080'     # Gri
}

current_category = 'happy'
emotion_history = []
emotion_window = deque(maxlen=3)
@app.route('/')
def index():
    """Pagina principală"""
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Procesează un frame primit de la client"""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data'}), 400

        # Decodare imagine base64
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode image'}), 400

        # Detectare emoție
        detector = get_current_detector()
        emotion, confidence, face_coords = detector.detect_emotion(frame)

        # Logică de netezire: Mediază detectarea emoțiilor
        global emotion_window
        emotion_window.append((emotion, confidence))
        
        # Determină emoția logică bazată pe istoricul recent
        emotions = [e[0] for e in emotion_window]
        if emotions:
            final_emotion = Counter(emotions).most_common(1)[0][0]
        else:
            final_emotion = emotion
            
        # Calculează încrederea medie pentru emoția dominantă
        confidences = [e[1] for e in emotion_window if e[0] == final_emotion]
        final_confidence = sum(confidences) / len(confidences) if confidences else confidence

        # Actualizare istoric
        global emotion_history
        emoji = random.choice(EMOJI_CATEGORIES.get(final_emotion, EMOJI_CATEGORIES['neutral']))
        
        emotion_history.append({
            'emotion': final_emotion,
            'confidence': float(final_confidence),
            'timestamp': datetime.now().isoformat()
        })
        
        if len(emotion_history) > 50:
            emotion_history.pop(0)

        response_data = {
            'emotion': final_emotion,
            'confidence': float(final_confidence),
            'emoji': emoji,
            'timestamp': datetime.now().isoformat(),
            'color': EMOTION_COLORS.get(final_emotion, '#ffffff')
        }

        if face_coords:
            response_data['face_coordinates'] = {
                'x': face_coords[0],
                'y': face_coords[1],
                'w': face_coords[2],
                'h': face_coords[3]
            }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_emotion')
def get_emotion():
    """Obține ultima emoție detectată (pentru compatibilitate sau polling secundar)"""
    if not emotion_history:
        return jsonify({
            'emotion': 'neutral', 
            'confidence': 0.0, 
            'emoji': '😐', 
            'timestamp': datetime.now().isoformat()
        })
    
    last_entry = emotion_history[-1]
    # Re-preia emoji doar în caz sau folosește unul stocat? logica spune să returnăm ultima stare.
    # Vom returna doar ultima intrare plus un emoji.
    emoji = random.choice(EMOJI_CATEGORIES.get(last_entry['emotion'], EMOJI_CATEGORIES['neutral']))
    return jsonify({
        'emotion': last_entry['emotion'],
        'confidence': last_entry['confidence'],
        'emoji': emoji,
        'timestamp': last_entry['timestamp']
    })

@app.route('/get_emoji/<emotion>')
def get_emoji(emotion):
    """Obține un emoji aleatoriu pentru o emoție"""
    emoji = random.choice(EMOJI_CATEGORIES.get(emotion, EMOJI_CATEGORIES['neutral']))
    return jsonify({'emoji': emoji})

@app.route('/change_category', methods=['POST'])
def change_category():
    """Schimbă categoria activă de emoji-uri"""
    global current_category
    data = request.get_json()
    category = data.get('category', 'happy')
    
    if category in EMOJI_CATEGORIES:
        current_category = category
        return jsonify({'success': True, 'category': current_category})
    
    return jsonify({'success': False, 'error': 'Categorie invalidă'}), 400

@app.route('/get_history')
def get_history():
    """Obține istoricul emoțiilor"""
    return jsonify({'history': emotion_history})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Șterge istoricul emoțiilor"""
    global emotion_history
    emotion_history = []
    return jsonify({'success': True})

@app.route('/switch_model', methods=['POST'])
def switch_model():
    """Schimbă modelul de detectare activ"""
    global current_model_name
    data = request.json
    model = data.get('model')
    
    if model in detectors:
        current_model_name = model
        return jsonify({'success': True, 'model': current_model_name})
    
    return jsonify({'error': 'Invalid model or model not available', 'available': list(detectors.keys())}), 400

@app.route('/get_models')
def get_models():
    """Returnează modelele disponibile și cel activ"""
    return jsonify({
        'models': list(detectors.keys()),
        'current': current_model_name
    })

@app.route('/save_capture', methods=['POST'])
def save_capture():
    """Salvează o captură cu emoția detectată"""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data'}), 400

        # Decodare imagine base64
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode image'}), 400
    
        detector = get_current_detector()
        emotion, confidence, _ = detector.detect_emotion(frame)
        frame = detector.draw_results(frame, emotion, confidence)
        
        # Creează directorul pentru capturi dacă nu există
        captures_dir = 'static/captures'
        os.makedirs(captures_dir, exist_ok=True)
        
        # Salvează imaginea
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'capture_{emotion}_{timestamp}.jpg'
        filepath = os.path.join(captures_dir, filename)
        cv2.imwrite(filepath, frame)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'emotion': emotion,
            'confidence': float(confidence)
        })
    except Exception as e:
        print(f"Error saving capture: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Endpoint de verificare a stării"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = os.environ.get('FLASK_PORT', '5000')
    
    print("🎭 Emotion Detection System")
    print("📡 Server running on http://{}:{}".format(host, port))
    print("🎥 Camera access required")
    app.run(debug=True, threaded=True, host=host, port=port)
