# 🎭 Emotion Detection System

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Sistem avansat de detectare a emoțiilor în timp real folosind AI, OpenCV și Flask**

[Demo](#demo) • [Instalare](#instalare) • [Utilizare](#utilizare) • [Documentație](#documentație)

</div>

---

## 📋 Cuprins

- [Despre Proiect](#despre-proiect)
- [Funcționalități](#funcționalități)
- [Arhitectura Sistemului](#arhitectura-sistemului)
- [Instalare](#instalare)
- [Configurare](#configurare)
- [Utilizare](#utilizare)
- [Structura Proiectului](#structura-proiectului)
- [Tehnologii](#tehnologii)
- [Depanare](#depanare)
- [Contribuții](#contribuții)

---

## 🎯 Despre Proiect

**Emotion Detection System** este o aplicație web interactivă care folosește inteligență artificială pentru a detecta și analiza emoțiile umane în timp real prin intermediul camerei web. Sistemul oferă:

- ✅ Detectare în timp real a 5 emoții principale
- ✅ Interfață modernă și intuitivă
- ✅ Feedback vizual instant cu emoji-uri animate
- ✅ Grafice istorice pentru analiza emoțiilor
- ✅ Posibilitate de salvare a capturilor

---

## ⭐ Funcționalități

### 🎥 Detectare în Timp Real
- Stream video live de la camera web
- Detectare automată a fețelor
- Clasificare instantanee a emoțiilor
- Scoruri de încredere pentru fiecare detecție

### 😊 5 Categorii de Emoții
1. **Happy** (Fericit) - 😊
2. **Sad** (Trist) - 😢
3. **Angry** (Furios) - 😠
4. **Surprise** (Surprins) - 😲
5. **Neutral** (Neutru) - 😐

### 🎨 Interfață Avansată
- Design modern și responsive
- Emoji-uri animate mari
- Bare de progres pentru încredere
- Culori dinamice bazate pe emoție
- Notificări toast pentru feedback

### 📊 Analiză și Istoric
- Grafic istoric al emoțiilor detectate
- Statistici în timp real
- Export de capturi cu emoții
- Resetare istoric

### 🔧 Moduri de Funcționare
- **Mod Manual**: Detectare la cerere
- **Mod Automat**: Detectare continuă (la fiecare 3 secunde)
- **Mod Categorie**: Schimbare manuală a categoriilor de emoji

---

## 🏗️ Arhitectura Sistemului

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Video Feed  │  │ Emoji Display │  │   Controls   │  │
│  │   Component  │  │   Component   │  │   Component  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          │        HTTP/REST API (CORS)         │
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────┐
│                    BACKEND (Flask)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Emotion Detection Engine                  │   │
│  │  ┌─────────────┐      ┌──────────────────────┐  │   │
│  │  │   OpenCV    │─────▶│  Face Detection      │  │   │
│  │  │   Camera    │      │  (Haar Cascade)      │  │   │
│  │  └─────────────┘      └──────────┬───────────┘  │   │
│  │                                   │              │   │
│  │                       ┌───────────▼───────────┐  │   │
│  │                       │   AI Model / Simulator │  │   │
│  │                       │   (TensorFlow/Keras)   │  │   │
│  │                       └───────────┬───────────┘  │   │
│  │                                   │              │   │
│  │                       ┌───────────▼───────────┐  │   │
│  │                       │  Emotion Classification │  │   │
│  │                       │  + Confidence Score     │  │   │
│  │                       └─────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalare

### Cerințe Preliminare

- **Python 3.8+** instalat
- **pip** (Python package manager)
- **Camera web** funcțională
- **Browser modern** (Chrome, Firefox, Edge)

### Pași de Instalare

#### 1. Clonează/Descarcă Proiectul

```bash
git clone https://github.com/yourusername/emotion-detection-system.git
cd emotion-detection-system
```

#### 2. Instalează Backend-ul

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Instalează dependențele
pip install -r requirements.txt
```

#### 3. (Opțional) Descarcă Modelul Pre-antrenat

Pentru detectare mai precisă, poți descărca un model antrenat:

**Model FER2013:**
```bash
# Descarcă de la:
# https://github.com/oarriaga/face_classification/releases

# Plasează fișierul în:
backend/models/emotion_model.h5
```

> **Notă**: Sistemul funcționează și fără model (folosește detectare simulată bazată pe caracteristici ale imaginii).

---

## ⚙️ Configurare

### Structura Directorului

Asigură-te că ai următoarea structură:

```
emotion-detection-system/
│
├── backend/
│   ├── app.py                    # Flask server
│   ├── emotion_detector.py       # Logica de detectare
│   ├── requirements.txt          # Dependențe Python
│   └── models/
│       └── emotion_model.h5      # Model AI (opțional)
│
├── frontend/
│   ├── index.html                # Pagina principală
│   ├── css/
│   │   └── style.css             # Stiluri
│   ├── js/
│   │   └── main.js               # Logică frontend
│   ├── assets/
│   │   ├── emojis/               # Imagini emoji (opțional)
│   │   └── sounds/               # Sunete (opțional)
│   └── captures/                 # Capturi salvate
│
└── README.md
```

### Configurare CORS

Backend-ul este configurat automat cu CORS pentru a permite comunicarea cu frontend-ul.

---

## 📖 Utilizare

### 1. Pornește Backend-ul

```bash
cd backend
python app.py
```

Vei vedea:
```
🎭 Emotion Detection System - Backend
📡 Server running on http://localhost:5000
🎥 Camera access required
```

### 2. Deschide Frontend-ul

**Metoda 1: Direct în Browser**
```bash
# Navighează la directorul frontend
cd frontend

# Deschide index.html în browser
# Pe Windows:
start index.html

# Pe macOS:
open index.html

# Pe Linux:
xdg-open index.html
```

**Metoda 2: Server Local**
```bash
cd frontend
python -m http.server 8000

# Accesează: http://localhost:8000
```

### 3. Folosește Aplicația

1. **Permite accesul la cameră** când browser-ul solicită
2. **Apasă "Detect Emotion"** pentru detectare manuală
3. **SAU** activează **"Start Auto-Detect"** pentru detectare continuă
4. **Vezi rezultatele** în timp real:
   - Emoji animat mare
   - Nume emoție
   - Scor de încredere
5. **Explorează funcționalitățile**:
   - 📸 Salvează capturi
   - 📊 Vezi istoricul grafic
   - 🎭 Schimbă categoriile de emoji
   - 🗑️ Șterge istoricul

---

## 🛠️ Depanare

### Camera nu funcționează?

**Soluții:**
- Verifică permisiunile browser-ului pentru camera web
- Asigură-te că nicio altă aplicație folosește camera
- Încearcă alt browser (Chrome este recomandat)
- Pe Windows: Verifică setările de confidențialitate

### Backend nu pornește?

**Soluții:**
```bash
# Reinstalează dependențele
pip install -r requirements.txt --force-reinstall

# Verifică versiunea Python
python --version  # Trebuie să fie 3.8+

# Verifică dacă portul 5000 este liber
# Windows:
netstat -ano | findstr :5000

# Linux/macOS:
lsof -i :5000
```

### "Cannot connect to backend"?

**Soluții:**
- Asigură-te că backend-ul rulează pe `http://localhost:5000`
- Verifică firewall-ul/antivirus-ul
- Deschide consola browser-ului (F12) pentru erori CORS
- Verifică că `Flask-CORS` este instalat

### Modelul nu se încarcă?

**Soluții:**
- Verifică dacă `emotion_model.h5` există în `backend/models/`
- Sistemul va funcționa automat în modul simulare
- Verifică versiunea TensorFlow:
```bash
pip show tensorflow
```

### Erori la instalare pe Windows?

**Soluții:**
```bash
# Actualizează pip
python -m pip install --upgrade pip

# Instalează Visual C++ Build Tools dacă cerut
# Descarcă de la: https://visualstudio.microsoft.com/downloads/

# Instalează dependențele individual
pip install Flask Flask-CORS opencv-python numpy
```

---

## 🔧 Tehnologii Utilizate

### Backend
- **Python 3.8+** - Limbaj de programare
- **Flask 3.0** - Framework web
- **Flask-CORS** - Suport CORS
- **OpenCV 4.8** - Procesare imagini și video
- **TensorFlow 2.15** - Machine learning (opțional)
- **NumPy** - Calcul numeric

### Frontend
- **HTML5** - Structură
- **CSS3** - Stilizare modernă
- **JavaScript (ES6+)** - Logică interactivă
- **Chart.js** - Vizualizare date
- **Fetch API** - Comunicare cu backend

### AI & Computer Vision
- **Haar Cascade** - Detectare fețe
- **CNN Model** - Clasificare emoții (opțional)
- **Image Processing** - Preprocesare imagini

---

## 📊 Performanță

- ⚡ **Detectare**: ~50-100ms per frame
- 🎥 **FPS Video**: 25-30 FPS
- 💾 **Memorie**: ~200-500MB RAM
- 🔄 **Auto-detect**: La fiecare 3 secunde
- 📈 **Istoric**: Ultimele 50 detecții

---

## 🎓 Cum Funcționează?

### 1. Capturare Video
```python
camera = cv2.VideoCapture(0)
success, frame = camera.read()
```

### 2. Detectare Față
```python
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
```

### 3. Preprocesare
```python
face_img = cv2.resize(face_roi, (48, 48))
face_img = face_img / 255.0
```

### 4. Clasificare Emoție
```python
predictions = model.predict(face_img)
emotion = emotions[np.argmax(predictions)]
```

### 5. Afișare Rezultate
```javascript
updateEmotionDisplay(emotion, confidence)
```

---

## 🚀 Îmbunătățiri Viitoare

- [ ] Suport pentru multiple fețe simultan
- [ ] Detectare emoții din voce
- [ ] Exportare rapoarte PDF
- [ ] API RESTful complet documentat
- [ ] Bază de date pentru istoric persistent
- [ ] Autentificare utilizatori
- [ ] Dashboard administrativ
- [ ] Suport pentru streaming live
- [ ] Aplicație mobilă (React Native)
- [ ] Model custom antrenat

---

## 🤝 Contribuții

Contribuțiile sunt binevenite! Pentru a contribui:

1. Fork proiectul
2. Creează un branch: `git checkout -b feature/NewFeature`
3. Commit: `git commit -m 'Add NewFeature'`
4. Push: `git push origin feature/NewFeature`
5. Deschide un Pull Request

---

## 📝 Licență

Acest proiect este open-source și disponibil sub licența MIT.

---

## 👨‍💻 Autor

Dezvoltat pentru demonstrarea capabilităților AI în detectarea emoțiilor.

---

## 📞 Suport

Pentru probleme sau întrebări:
- 🐛 Deschide un **Issue** pe GitHub
- 📧 Email: support@example.com
- 💬 Discord: [Join Server](#)

---

## ⭐ Apreciere

Dacă acest proiect te-a ajutat, lasă un ⭐ pe GitHub!

---

<div align="center">

**Made with ❤️ and 🤖**

[⬆ Back to Top](#-emotion-detection-system)

</div>
