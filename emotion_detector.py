import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

class EmotionDetector:
    def __init__(self, model_path='models/emotion_model.h5'):
        """Inițializează detectorul de emoții"""
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        # Mapare la categoriile noastre (5 emoții principale)
        self.emotion_mapping = {
            'angry': 'angry',
            'disgust': 'angry',
            'fear': 'sad',
            'happy': 'happy',
            'sad': 'sad',
            'surprise': 'surprise',
            'neutral': 'neutral'
        }
        
        # Încarcă modelul dacă există
        if os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
                self.model_loaded = True
            except:
                print(f"Eroare la încărcarea modelului din {model_path}")
                self.model_loaded = False
        else:
            print(f"Modelul nu a fost găsit la {model_path}")
            print("Se va folosi detectarea simulată.")
            self.model_loaded = False
        
        # Încarcă clasificatorul Haar Cascade pentru detectarea fețelor
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def preprocess_face(self, face_img):
        """Preprocesează imaginea feței pentru model"""
        # Redimensionează la 48x48 (dimensiunea standard pentru modele de emoții)
        face_img = cv2.resize(face_img, (48, 48))
        
        # Convertește la grayscale dacă este color
        if len(face_img.shape) == 3:
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # Normalizează
        face_img = face_img / 255.0
        
        # Adaugă dimensiuni pentru batch și canal
        face_img = np.expand_dims(face_img, axis=0)
        face_img = np.expand_dims(face_img, axis=-1)
        
        return face_img
    
    def detect_emotion(self, frame):
        """Detectează emoția din cadrul video"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return 'neutral', 0.0
        
        # Folosește prima față detectată
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        if self.model_loaded:
            # Folosește modelul real
            face_img = self.preprocess_face(face_roi)
            predictions = self.model.predict(face_img, verbose=0)
            emotion_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_idx])
            emotion = self.emotions[emotion_idx]
            
            # Mapează la categoriile noastre
            emotion = self.emotion_mapping.get(emotion, 'neutral')
        else:
            # Simulare: detectare bazată pe caracteristici simple
            emotion, confidence = self.simulate_emotion_detection(face_roi)
        
        return emotion, confidence
    
    def simulate_emotion_detection(self, face_roi):
        """Simulează detectarea emoțiilor pe baza caracteristicilor simple"""
        # Calculează brightness-ul mediu
        brightness = np.mean(face_roi)
        
        # Calculează contrastul
        contrast = np.std(face_roi)
        
        # Logică simplă de clasificare
        if brightness > 140 and contrast > 50:
            return 'happy', 0.75
        elif brightness < 100:
            return 'sad', 0.70
        elif contrast > 60:
            return 'surprise', 0.65
        elif brightness > 130:
            return 'neutral', 0.60
        else:
            return 'angry', 0.68
    
    def draw_results(self, frame, emotion, confidence):
        """Desenează rezultatele pe cadrul video"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            # Desenează dreptunghi în jurul feței
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Adaugă text cu emoția și încrederea
            text = f'{emotion.upper()}: {confidence:.2%}'
            cv2.putText(
                frame, 
                text, 
                (x, y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.9, 
                (0, 255, 0), 
                2
            )
        
        return frame
    
    def get_emotion_color(self, emotion):
        """Returnează culoarea asociată emoției"""
        colors = {
            'happy': (0, 255, 0),    # Verde
            'sad': (255, 0, 0),       # Albastru
            'angry': (0, 0, 255),     # Roșu
            'surprise': (255, 255, 0), # Cyan
            'neutral': (128, 128, 128) # Gri
        }
        return colors.get(emotion, (255, 255, 255))
