# 🎭 Emotion Detecting System

Sistem avansat de detectare a emoțiilor în timp real folosind AI, OpenCV și Flask.

## 📋 Cerințe de Sistem

- Python 3.8 sau mai nou
- Camera web funcțională
- Sistem de operare: Windows, macOS sau Linux

## 🚀 Instalare

### 1. Clonează/Descarcă proiectul

```bash
git clone <repository-url>
cd emotion-detection-system
```

### 2. Creează un mediu virtual (recomandat)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalează dependențele

```bash
pip install -r requirements.txt
```

### 4. Descarcă modelul pre-antrenat (OPȚIONAL)

Pentru detectare mai precisă, descarcă un model pre-antrenat:

**Opțiune A: Model FER2013**
- Descarcă de la: https://github.com/oarriaga/face_classification/blob/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5
- Redenumește în `emotion_model.h5`
- Plasează în directorul `models/`

**Opțiune B: Model propriu**
- Antrenează propriul model pe datasetul FER2013
- Salvează ca `emotion_model.h5` în `models/`

**Notă**: Dacă nu folosești un model, sistemul va funcționa cu detectare simulată bazată pe caracteristici simple.

## 📁 Structura Directorului

Asigură-te că ai următoarea structură:

```
emotion-detection-system/
│
├── app.py
├── emotion_detector.py
├── requirements.txt
├── README.md
│
├── models/
│   └── emotion_model.h5 (opțional)
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   ├── sounds/
│   │   ├── happy.mp3
│   │   ├── sad.mp3
│   │   ├── angry.mp3
│   │   ├── surprise.mp3
│   │   └── neutral.mp3
│   └── captures/
│
└── templates/
    └── index.html
```

## 🎵 Adăugarea Sunetelor (OPȚIONAL)

Pentru funcționalitatea completă, adaugă fișiere audio MP3 în `static/sounds/`:
- `happy.mp3` - sunet vesel
- `sad.mp3` - sunet trist
- `angry.mp3` - sunet furios
- `surprise.mp3` - sunet surpriză
- `neutral.mp3` - sunet neutru

Poți găsi sunete gratuite pe:
- https://freesound.org
- https://mixkit.co/free-sound-effects/

## ▶️ Rularea Aplicației

### Pornește serverul Flask:

```bash
python app.py
```

### Accesează aplicația:

Deschide browser-ul și navighează la:
```
http://localhost:5000
```

## 🎯 Cum să Folosești

1. **Permite accesul la cameră** când browser-ul solicită permisiunea
2. **Apasă "Detectează Emoția"** pentru a analiza expresia facială
3. **Vezi rezultatele** - emoji, emoție și scor de încredere
4. **Explorează funcționalitățile**:
   - Schimbă categoriile de emoji
   - Salvează capturi cu emoțiile detectate
   - Vizualizează istoricul în grafic
   - Șterge istoricul când dorești

## 🛠️ Funcționalități

### ✨ Principale
- ✅ Detectare emoții în timp real
- ✅ 5 categorii de emoții: fericit, trist, furios, surprins, neutru
- ✅ Scoruri de încredere pentru fiecare detecție
- ✅ Emoji-uri animate corespunzătoare fiecărei emoții

### 📊 Avansate
- ✅ Grafic istoric al emoțiilor
- ✅ Salvare capturi cu emoția detectată
- ✅ Redare sunete pentru fiecare emoție
- ✅ Schimbare categorii de emoji
- ✅ Interfață responsive (mobile-friendly)

## 🔧 Depanare

### Camera nu funcționează?
- Verifică permisiunile browserului
- Asigură-te că nicio altă aplicație folosește camera
- Încearcă alt browser (Chrome, Firefox, Edge)

### Modelul nu se încarcă?
- Verifică dacă fișierul `emotion_model.h5` există în `models/`
- Sistemul va funcționa și fără model (detectare simulată)
- Verifică versiunea TensorFlow

### Erori la instalare?
```bash
# Încearcă actualizarea pip
python -m pip install --upgrade pip

# Reinstalează dependențele
pip install -r requirements.txt --force-reinstall
```

## 📚 Tehnologii Utilizate

- **Python 3.8+** - Limbaj de programare
- **Flask** - Framework web
- **OpenCV** - Procesare imagini și video
- **TensorFlow/Keras** - Machine learning
- **Chart.js** - Vizualizare date
- **HTML/CSS/JavaScript** - Frontend

## 🎓 Arhitectura Sistemului

```
┌─────────────────┐
│  Camera Web     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenCV         │◄──┐
│  (Detectare     │   │
│   Fețe)         │   │
└────────┬────────┘   │
         │            │
         ▼            │
┌─────────────────┐   │
│  Model AI       │   │
│  (Clasificare   │   │
│   Emoții)       │   │
└────────┬────────┘   │
         │            │
         ▼            │
┌─────────────────┐   │
│  Flask Backend  │───┘
│  (Logică +      │
│   API)          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Interfață Web  │
│  (Afișare       │
│   Rezultate)    │
└─────────────────┘
```

## 🚀 Îmbunătățiri Viitoare

- [ ] Suport pentru multiple fețe simultan
- [ ] Detectare emoții din voce
- [ ] Export rapoarte PDF
- [ ] Integrare baze de date pentru istoric persistent
- [ ] API RESTful pentru integrare cu alte aplicații
- [ ] Suport pentru streaming live

## 📝 Licență

Acest proiect este open-source și disponibil pentru uz educațional.

## 👨‍💻 Autor

Proiect dezvoltat pentru demonstrarea capabilităților de detectare a emoțiilor folosind AI.

## 🤝 Contribuții

Contribuțiile sunt binevenite! Simte-te liber să:
1. Fork-uiești proiectul
2. Creezi un branch pentru feature-ul tău
3. Commit-uiești modificările
4. Push-uiești pe branch
5. Deschizi un Pull Request

## 📞 Suport

Pentru probleme sau întrebări:
- Deschide un issue pe GitHub
- Verifică documentația
- Consultă secțiunea de Depanare

---

**Enjoy detecting emotions! 🎭😊**
