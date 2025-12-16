import cv2
import numpy as np
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
        self.model_loaded = False
        if os.path.exists(model_path):
            try:
                from tensorflow.keras.models import load_model
                self.model = load_model(model_path)
                self.model_loaded = True
                print("✅ Model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")
                print("Using simulation mode...")
                self.model_loaded = False
        else:
            print(f"⚠️ Model not found at {model_path}")
            print("Using simulation mode...")
            self.model_loaded = False
        
        # Încarcă clasificatorul Haar Cascade pentru detectarea fețelor
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            print("❌ Error: Could not load face cascade classifier!")
    
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
        
        # Folosește prima față detectată (sau cea mai mare)
        if len(faces) > 1:
            # Sortează după dimensiune (cea mai mare față)
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        if self.model_loaded:
            # Folosește modelul real
            try:
                face_img = self.preprocess_face(face_roi)
                predictions = self.model.predict(face_img, verbose=0)
                emotion_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][emotion_idx])
                emotion = self.emotions[emotion_idx]
                
                # Mapează la categoriile noastre
                emotion = self.emotion_mapping.get(emotion, 'neutral')
            except Exception as e:
                print(f"Error in model prediction: {e}")
                emotion, confidence = self.simulate_emotion_detection(face_roi)
        else:
            # Simulare: detectare bazată pe caracteristici simple
            emotion, confidence = self.simulate_emotion_detection(face_roi)
        
        return emotion, confidence
    
    def simulate_emotion_detection(self, face_roi):
        """
        Simulează detectarea emoțiilor pe baza caracteristicilor simple
        Această metodă este folosită când nu avem un model antrenat
        """
        # Calculează brightness-ul mediu
        brightness = np.mean(face_roi)
        
        # Calculează contrastul (deviația standard)
        contrast = np.std(face_roi)
        
        # Calculează histograma pentru a detecta distribuția tonurilor
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist_normalized = hist.ravel() / hist.sum()
        
        # Calculează entropia (măsură a complexității)
        entropy = -np.sum(hist_normalized * np.log2(hist_normalized + 1e-10))
        
        # Logică de clasificare bazată pe multiple caracteristici
        if brightness > 135 and contrast > 50 and entropy > 6.5:
            return 'happy', 0.72 + (brightness - 135) * 0.001
        elif brightness < 100 and contrast < 40:
            return 'sad', 0.68 + (100 - brightness) * 0.001
        elif contrast > 65 and entropy > 7.0:
            return 'surprise', 0.70 + (contrast - 65) * 0.002
        elif brightness < 110 and contrast > 55:
            return 'angry', 0.65 + (contrast - 55) * 0.002
        else:
            return 'neutral', 0.60 + entropy * 0.01
    
    def draw_results(self, frame, emotion, confidence):
        """Desenează rezultatele pe cadrul video"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            # Culoare în funcție de emoție
            color = self.get_emotion_color(emotion)
            
            # Desenează dreptunghi în jurul feței
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
            
            # Adaugă text cu emoția și încrederea
            text = f'{emotion.upper()}: {confidence:.1%}'
            
            # Fundal pentru text
            (text_width, text_height), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
            )
            cv2.rectangle(
                frame, 
                (x, y - text_height - 10), 
                (x + text_width, y), 
                color, 
                -1
            )
            
            # Text
            cv2.putText(
                frame, 
                text, 
                (x, y - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (255, 255, 255), 
                2
            )
            
            # Adaugă emoji în colț
            emoji = self.get_emotion_emoji(emotion)
            cv2.putText(
                frame,
                emoji,
                (x + w - 40, y + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                color,
                2
            )
        
        return frame
    
    def get_emotion_color(self, emotion):
        """Returnează culoarea BGR asociată emoției"""
        colors = {
            'happy': (0, 255, 0),      # Verde
            'sad': (255, 0, 0),         # Albastru
            'angry': (0, 0, 255),       # Roșu
            'surprise': (255, 255, 0),  # Cyan
            'neutral': (128, 128, 128)  # Gri
        }
        return colors.get(emotion, (255, 255, 255))
    
    def get_emotion_emoji(self, emotion):
        """Returnează reprezentarea text a emoji-ului"""
        emojis = {
            'happy': ':)',
            'sad': ':(',
            'angry': '>:(',
            'surprise': ':O',
            'neutral': ':|'
        }
        return emojis.get(emotion, ':|')
