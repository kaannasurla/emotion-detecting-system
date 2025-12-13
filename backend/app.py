from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from emotion_detector import EmotionDetector
import json
import random
import os
from datetime import datetime
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS pentru frontend separat

emotion_detector = EmotionDetector()

# Configurare categorii emoji
EMOJI_CATEGORIES = {
    'happy': ['😊', '😄', '🤗', '😁', '🥳', '😍', '🌟'],
    'sad': ['😢', '😔', '😞', '😿', '💔', '😭', '☹️'],
    'angry': ['😠', '😡', '🤬', '👿', '💢', '😤', '💥'],
    'surprise': ['😲', '😮', '🤯', '😳', '🎊', '✨', '🎉'],
    'neutral': ['😐', '😑', '🙂', '😶', '😏', '🤔', '😌']
}

current_category = 'happy'
emotion_history = []
camera = None

def get_camera():
    """Obține instanța camerei"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera

@app.route('/video_feed')
def video_feed():
    """Stream video cu detectarea emoțiilor"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    """Generează cadre video cu detectarea emoțiilor"""
    cam = get_camera()
    
    while True:
        success, frame = cam.read()
        if not success:
            break
        
        # Flip horizontal pentru efect oglindă
        frame = cv2.flip(frame, 1)
        
        # Detectează emoția
        emotion, confidence = emotion_detector.detect_emotion(frame)
        
        # Desenează rezultatele pe cadru
        frame = emotion_detector.draw_results(frame, emotion, confidence)
        
        # Convertește cadrul în JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/get_emotion')
def get_emotion():
    """Obține emoția curentă detectată"""
    cam = get_camera()
    success, frame = cam.read()
    
    if not success:
        return jsonify({'error': 'Nu s-a putut accesa camera'}), 500
    
    # Flip horizontal
    frame = cv2.flip(frame, 1)
    
    emotion, confidence = emotion_detector.detect_emotion(frame)
    
    # Selectează emoji aleatoriu din categoria corespunzătoare
    emoji = random.choice(EMOJI_CATEGORIES.get(emotion, EMOJI_CATEGORIES['neutral']))
    
    # Adaugă în istoric
    emotion_history.append({
        'emotion': emotion,
        'confidence': float(confidence),
        'timestamp': datetime.now().isoformat()
    })
    
    # Păstrează doar ultimele 50 de înregistrări
    if len(emotion_history) > 50:
        emotion_history.pop(0)
    
    return jsonify({
        'emotion': emotion,
        'confidence': float(confidence),
        'emoji': emoji,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/capture_frame')
def capture_frame():
    """Capturează un singur frame ca base64"""
    cam = get_camera()
    success, frame = cam.read()
    
    if not success:
        return jsonify({'error': 'Nu s-a putut accesa camera'}), 500
    
    # Flip horizontal
    frame = cv2.flip(frame, 1)
    
    # Convertește în JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        'success': True,
        'image': f'data:image/jpeg;base64,{frame_base64}'
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

@app.route('/save_capture', methods=['POST'])
def save_capture():
    """Salvează o captură cu emoția detectată"""
    cam = get_camera()
    success, frame = cam.read()
    
    if not success:
        return jsonify({'error': 'Nu s-a putut accesa camera'}), 500
    
    # Flip horizontal
    frame = cv2.flip(frame, 1)
    
    emotion, confidence = emotion_detector.detect_emotion(frame)
    frame = emotion_detector.draw_results(frame, emotion, confidence)
    
    # Creează directorul pentru capturi dacă nu există
    captures_dir = '../frontend/captures'
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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

if __name__ == '__main__':
    print("🎭 Emotion Detection System - Backend")
    print("📡 Server running on http://localhost:5000")
    print("🎥 Camera access required")
    app.run(debug=True, threaded=True, port=5000)