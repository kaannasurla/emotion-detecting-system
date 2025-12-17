import cv2
import numpy as np
import mediapipe as mp
import math

class EmotionDetector:
    def __init__(self):
        """Inițializează detectorul de emoții cu Mediapipe"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        
        # Culori pentru vizualizare
        self.colors = {
            'happy': (0, 255, 0),      # Verde
            'sad': (255, 0, 0),        # Albastru
            'angry': (0, 0, 255),      # Roșu
            'surprise': (255, 255, 0), # Cyan
            'neutral': (200, 200, 200) # Gri
        }

    def _get_distance(self, p1, p2):
        """Distanța euclidiană între două puncte normalizată prin coordonate"""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def detect_emotion(self, frame):
        """Detectează emoția folosind repere faciale"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        if not results.multi_face_landmarks:
            return 'neutral', 0.0, None

        landmarks = results.multi_face_landmarks[0].landmark
        
        # --- EXTRAGERE TRĂSĂTURI ---
        
        # 1. GURĂ (MAR - Raportul de Aspect al Gurii)
        # Sus: 13, Jos: 14, Stânga: 61, Dreapta: 291
        top_lip = landmarks[13]
        bottom_lip = landmarks[14]
        left_corner = landmarks[61]
        right_corner = landmarks[291]
        
        mouth_height = self._get_distance(top_lip, bottom_lip)
        mouth_width = self._get_distance(left_corner, right_corner)
        mar = mouth_height / mouth_width if mouth_width > 0 else 0
        
        # Verificare zâmbet: colțuri vs centru
        # Notă: Y crește în jos. Y mai mic înseamnă mai sus.
        center_y = (top_lip.y + bottom_lip.y) / 2
        corners_y = (left_corner.y + right_corner.y) / 2
        # Dacă colțurile sunt semnificativ mai sus decât centrul, este un zâmbet
        smile_ratio = (center_y - corners_y)
        
        # 2. OCHI (EAR - Raportul de Aspect al Ochilor)
        # Ochiul Stâng (din perspectiva privitorului? Nu, stânga subiectului este dreapta noastră de obicei, dar indicii MP sunt ficși)
        # Ochiul Stâng: 33 (interior), 133 (exterior), 159 (sus), 145 (jos)
        # Ochiul Drept: 362 (interior), 263 (exterior), 386 (sus), 374 (jos)
        
        # Ochiul Stâng EAR
        left_v = self._get_distance(landmarks[159], landmarks[145])
        left_h = self._get_distance(landmarks[33], landmarks[133])
        left_ear = left_v / left_h if left_h > 0 else 0
        
        # Ochiul Drept EAR
        right_v = self._get_distance(landmarks[386], landmarks[374])
        right_h = self._get_distance(landmarks[362], landmarks[263])
        right_ear = right_v / right_h if right_h > 0 else 0
        
        avg_ear = (left_ear + right_ear) / 2
        
        # 3. SPRÂNCENE
        # Sprânceana Stângă: 105 (mijloc), 107 (interior), 70 (lateral)
        # Sprânceana Dreaptă: 334 (mijloc), 336 (interior), 300 (lateral)
        # Tristețea implică adesea sprâncenele interioare mergând în SUS față de cele exterioare.
        # Dar simplu, fața "tristă" are adesea sprâncenele înclinate sus-interior.
        
        left_brow_inner = landmarks[107]
        left_brow_outer = landmarks[70]
        right_brow_inner = landmarks[336]
        right_brow_outer = landmarks[300]
        
        # Verifică panta: Interiorul ar trebui să fie mai sus (Y mai mic) decât exteriorul pentru forma de "tristețe" (V inversat)
        # Arc normal: Interiorul poate fi mai jos sau egal.
        # Să verificăm înălțimea relativă.
        
        left_brow_stress = (left_brow_inner.y - left_brow_outer.y)
        right_brow_stress = (right_brow_inner.y - right_brow_outer.y)
        
        # Dacă interiorul e mai sus (y mai mic), valoarea e negativă.
        # Dacă interiorul e mai jos (y mai mare), valoarea e pozitivă.
        # Tristețe -> Interiorul merge SUS -> valoarea devine mai negativă sau mai mică.
        
        # Calculează înălțimea medie a sprâncenelor?
        
        # Vom folosi un factor de "Sprânceană Tristă".
        # Dacă (Y Interior < Y Exterior) -> trăsătură distinctă de tristețe (sau surpriză, dar surpriza are gura deschisă)
        
        sad_brows = (left_brow_stress < 0.0) and (right_brow_stress < 0.0)

        # --- LOGICĂ CLASIFICARE ---
        
        # Praguri (ajustabile)
        emotion = 'neutral'
        confidence = 0.5
        
        # Modificare logică detecție furie - mai sensibil la sprâncene și ochi
        # Furie: Sprâncene coborâte (mai ales interior), ochi mijiți (EAR mic), gură strânsă sau încordată
        
        # Calculate brow simple average height or "frown" factor
        # Dacă interiorul sprâncenelor e mult mai JOS decât exteriorul -> FURIE (V shape)
        # Dacă interiorul e mult mai SUS -> TRISTEȚE / SURPRIZĂ (^ shape / sad brows)
        
        # right_brow_stress = inner.y - outer.y. 
        # inner.y > outer.y (pozitiv) înseamnă inner e mai JOS (furie)
        # inner.y < outer.y (negativ) înseamnă inner e mai SUS (tristețe)
        
        # HYPER SENSITIVE ANGER
        # Orice mică tendință de "V" la sprâncene ( > 0.0001 )
        is_frowning = (left_brow_stress > 0.0001) and (right_brow_stress > 0.0001)
        is_sad_brows = (left_brow_stress < -0.01) and (right_brow_stress < -0.01)

        # -------------------
        # LOGICA CLASIFICARE
        # -------------------

        # Fericit
        if smile_ratio > 0.015:
            emotion = 'happy'
            confidence = 0.8 + min(smile_ratio * 5, 0.2)
            
        # Surprins
        elif avg_ear > 0.35 and mar > 0.25:
            emotion = 'surprise'
            confidence = 0.8 + min((avg_ear - 0.35) * 4, 0.2)
            
        # Furios - HYPER SENSITIVE
        # Dacă există cea mai mică încruntare SAU ochi mijiți/gură strânsă (praguri foarte largi)
        elif is_frowning or (avg_ear < 0.30 and mar < 0.25):
             emotion = 'angry'
             confidence = 0.8 + (0.1 if is_frowning else 0)
             
        # Tristețe
        elif smile_ratio < -0.005 or is_sad_brows:
            emotion = 'sad'
            confidence = 0.6 + (0.1 if is_sad_brows else 0)
            
        else:
            emotion = 'neutral'
            confidence = 0.7
            
        # Rezervă pentru gură deschisă dar nu surpriză (poate fericit strigând?)
        if emotion == 'neutral' and mar > 0.5:
             emotion = 'surprise' # Sau fericit?
             
        return emotion, confidence, None

    def draw_results(self, frame, emotion, confidence):
        """Desenează rețeaua și informațiile pe cadru"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Desenează rețeaua
                self.drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.drawing_styles.get_default_face_mesh_tesselation_style()
                )
                
                # Desenează contururi
                self.drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.drawing_styles.get_default_face_mesh_contours_style()
                )

        # Desenează HUD
        h, w, _ = frame.shape
        color = self.colors.get(emotion, (255, 255, 255))
        
        # Casetă fundal
        cv2.rectangle(frame, (10, 10), (250, 110), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (250, 110), color, 2)
        
        # Text
        text = f"{emotion.upper()}"
        cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, color, 3)
        
        conf_text = f"Conf: {confidence:.2f}"
        cv2.putText(frame, conf_text, (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 1)
        
        return frame