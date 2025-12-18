# Emotion Detection System

Un sistem performant de detectare a emoțiilor în timp real, dezvoltat în Python folosind **MediaPipe** și **Flask**. Aplicația analizează fluxul video de la camera web pentru a identifica expresii faciale geometrice și le transpune instantaneu în emoji-uri animate sau imagini tematice.

## Cuprins
1. [Funcționalități Principale](#-funcționalități-principale)
2. [Tehnologii Utilizate](#-tehnologii-utilizate)
3. [Instalare și Configurare](#-instalare-și-configurare)
4. [Structura Proiectului](#-structura-proiectului)
5. [Depanare (Troubleshooting)](#-depanare-troubleshooting)

## Funcționalități Principale

### Detectare Inteligentă
*   **MediaPipe Face Mesh:** Utilizează 468 de puncte faciale 3D pentru o detectare precisă a geometriei feței, permițând identificarea subtilă a expresiilor (zâmbet, încruntare, surpriză) fără a necesita GPU dedicat.
*   **Mod Hibrid (Opțional):** Suportă integrarea modelelor deep learning (TensorFlow/Keras) pentru o clasificare bazată pe rețele neuronale convoluționale (CNN), dacă un model antrenat este prezent.

### Experiență Vizuală Interactivă
*   **Feedback Instant:** Afișează imaginea corespunzătoare emoției detectate în timp real.
*   **Biblioteci Tematice:** Comută între diferite pachete de imagini distractive (ex. Clash Royale, Florin Salam, Meme-uri) direct din interfață.
*   **Face Mesh Visualizer:** Un mod de debug vizual care suprapune rețeaua neuronală pe fața utilizatorului, util pentru a înțelege cum "vede" computerul fața.
*   **Indicatoare Vizuale:** Bounding box colorat dinamic în funcție de emoție (Verde=Fericit, Roșu=Furios, etc.) și afișarea scorului de încredere.

### Analiză și Date
*   **Monitorizare Emoțională:** Un grafic live urmărește evoluția emoțiilor detectate și nivelul de încredere al algoritmului.
*   **Istoric:** Păstrează un jurnal al detectărilor recente pentru analiză.
*   **Capturi Foto:** Funcție integrată pentru a salva momentele amuzante sau interesante direct pe disc în folderul `static/captures`.

## Tehnologii Utilizate

*   **Backend:** Python 3.8+, Flask, OpenCV, MediaPipe, NumPy.
*   **Frontend:** HTML5, Modern CSS, JavaScript (Vanilla), Chart.js.
*   **AI/ML:** MediaPipe Solutions (Default), TensorFlow (Opțional pentru modele custom).

## Instalare și Configurare

### Recomandat: Rulare cu Docker
Această metodă izolează aplicația, dar necesită configurarea accesului la cameră.

**Linux:**
```bash
# Construiește imaginea
docker build -t emotion-detection .

# Rulează containerul cu acces la video device
docker run -d -p 5000:5000 emotion-detection
```
### Alternativ: Rulare locală
Cerințe Preliminare
*   Python 3.8 sau mai nou instalat.
*   O cameră web funcțională conectată la calculator.

### 1. Clonare și Configurare Mediu
```bash
git clone <repository_url>
cd emotion-detecting-system

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalare Dependențe
```bash
pip install -r requirements.txt
```

### 3. Pornire Aplicație (Local)
```bash
python app.py
```
Serverul va porni la adresa `http://127.0.0.1:5000`. Accesați acest link în browser-ul preferat (Chrome sau Firefox recomandat).

> **Notă:** La prima rulare, browser-ul vă va cere permisiunea de a utiliza camera web.

## 📁 Structura Proiectului

O privire de ansamblu asupra fișierelor principale:

*   `app.py`: Nucleul aplicației web Flask. Gestionează rutele, procesarea imaginilor frame-by-frame și logica de backend.
*   `emotion_detector_mediapipe.py`: Modulul principal de detecție. Calculează distanțele dintre reperele faciale (ex. deschiderea gurii, poziția sprâncenelor) pentru a deduce emoția curentă.
*   `emotion_detector_tensorflow.py`: Modul alternativ pentru încărcarea modelelor clasice `.h5` (necesită fișier model în folderul `models/`).
*   `static/`: Conține resursele frontend-ului:
    *   `js/main.js`: Logica client-side care comunică cu backend-ul și actualizează interfața.
    *   `libraries/`: Colecții de imagini pentru diverse teme de afișare.
    *   `captures/`: Folderul unde se salvează capturile de ecran.
*   `templates/index.html`: Interfața utilizator principală.
*   `models/`: Folderul unde se salvează modelele clasice `.h5`.
*   `training/`: Scripturi pentru antrenarea modelelor. (Vezi training/README.md)

## Depanare (Troubleshooting)

*   **Camera nu pornește:**
    *   Asigurați-vă că nicio altă aplicație (Zoom, Teams, Skype) nu folosește camera în acel moment.
    *   Verificați dacă ați acordat permisiuni browser-ului.
    *   Pe Linux, verificați dacă utilizatorul are drepturi de acces la `/dev/video0`.

*   **Detecția este instabilă:**
    *   Asigurați-vă că fața este bine luminată din față. Lumina din spate (contre-jour) poate afecta precizia.
    *   Păstrați o distanță optimă de cameră (50-70 cm).

*   **Eroare TensorFlow / Lipsă Model:**
    *   Dacă primiți erori legate de `tensorflow` și nu aveți un model `.h5`, ignorați-le. Aplicația este configurată să folosească automat MediaPipe (care este mai rapid și mai robust pentru utilizare generală) dacă modelul dedicat lipsește.
