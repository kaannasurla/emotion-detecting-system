# 🔧 Troubleshooting - Sistemul de Biblioteci de Imagini

## ❓ Probleme Frecvente și Soluții

### 1. Butoanele bibliotecilor nu apar

**Simptom:** Secțiunea bibliotecilor este goală

**Cauze posibile:**
- Endpoint `/get_libraries` nu răspunde
- Eroare în JavaScript `loadLibraries()`

**Soluție:**
```bash
# 1. Verifică consola browserului (F12 > Console)
# 2. Caută erori de rețea (Network tab)
# 3. Verifică că serverul Flask rulează
curl http://localhost:5000/get_libraries
# Ar trebui să returneze:
# {"current":"clash_royale","libraries":["clash_royale","monkey","florin_salam"]}
```

---

### 2. Imaginile nu se afișează, doar emoji-ul

**Simptom:** Se afișează emoji fallback în loc de imagine

**Cauze posibile:**
- Calea imaginii nu e validă
- Fișierul imaginii lipsește
- Nume emoție nu se mapează corect

**Soluție:**
```bash
# 1. Verifică că dosarele și fișierele există
ls -la /home/neaguandrei05/tema_IA4/emotion-detecting-system/static/libraries/clash_royale/

# 2. Verifică consola browserului pentru erori 404
# 3. Verifica că extensiile sunt în lista acceptate (png, jpg, jpeg, gif, webp)
# 4. Verifica hogy nighel numelor imaginilor:
#    - happy.jpg (nu happy.JPG)
#    - Must lowercase for emotions
```

---

### 3. Eroare: "Bibliotecă invalidă"

**Simptom:** La selectarea unei biblioteci, apare mesaj de eroare

**Cauze posibile:**
- Biblioteca nu e adăugată la dicționarul `LIBRARIES`
- Nume biblioteca nu se potrivește exact

**Soluție:**
```python
# Verifica LIBRARIES din app.py
LIBRARIES = {
    'clash_royale': 'static/libraries/clash_royale',  # ← trebuie exact aceste numere
    'monkey': 'static/libraries/monkey',
    'florin_salam': 'static/libraries/florin_salam'
}

# Dacă ai adăugat o nouă bibliotecă, verifica:
# 1. Denumirea match EXACT
# 2. Folderul există
# 3. Calea e corectă (relativ la rădăcina proiectului)
# 4. Restart Flask
```

---

### 4. Imaginile se schimbă dar e întârziere

**Simptom:** Delay între schimbarea bibliotecii și afișarea imaginilor noi

**Cauze:**
- Cache browserului
- Interval polling prea mare

**Soluție:**
```javascript
// În main.js, modifică POLLING_INTERVAL dacă e necesar
const POLLING_INTERVAL = 500;  // îi 500ms în loc de 1000ms (mai rapid)

// Curăță cache browserului
// Chrome: Ctrl+Shift+Delete
// Firefox: Ctrl+Shift+Delete
```

---

### 5. Consola afișează: "Cannot read property 'emotionImage' of null"

**Simptom:** Eroare JavaScript la încărcare

**Cauze:**
- Element cu ID `emotionImage` nu există în HTML
- JavaScript se execută înainte ca DOM să fie pregătit

**Soluție:**
```html
<!-- Verifica că în index.html exista: -->
<div id="emotionImageDisplay">
    <img id="emotionImage" src="" alt="Emotion">
    <div id="fallbackEmoji">😐</div>
</div>

<!-- Restart aplicația -->
```

---

### 6. La switch library, imaginile rămân la fel

**Simptom:** Schimb biblioteca dar imaginile nu se actualizează

**Cauze:**
- `processFrame()` nu se apelează după schimbare
- `current_library` nu se actualizează corect

**Soluție:**
```javascript
// În switchLibrary(), asigură-te că exista:
loadLibraries();          // Reîncarcă butoanele
processFrame();           // Forțează detectare nouă

// Verifica endpoint-ul
fetch('/switch_library', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({library: 'monkey'})
}).then(r => r.json()).then(console.log);
```

---

### 7. Eroare: 404 /static/libraries/...

**Simptom:** Consola afișează errori 404 pentru imagini

**Cauze:**
- Imaginea nu există la calea returnată
- Calea e incorectă

**Soluție:**
```bash
# Verifică structura exactă:
tree /home/neaguandrei05/tema_IA4/emotion-detecting-system/static/libraries/

# Trebuie să arate:
# libraries/
# ├── clash_royale/
# │   ├── happy.jpg
# │   ├── sad.jpg
# │   ├── angry.png
# │   ├── surprise.png
# │   └── neutral.webp
# ├── monkey/
# └── florin_salam/

# Daca lipsesc, copiaza din foldere date originale:
cp /home/neaguandrei05/tema_IA4/clash_royale/* /home/neaguandrei05/tema_IA4/emotion-detecting-system/static/libraries/clash_royale/
```

---

### 8. Server returneaza: "No image for emotion"

**Simptom:** Backend nu gaseste imaginea

**Cauze:**
- Emoția nu e în mapping-ul `EMOTION_FILENAMES`
- Nume emoției din detector nu se potrivește

**Soluție:**
```python
# Verifica EMOTION_FILENAMES din app.py
EMOTION_FILENAMES = {
    'happy': 'happy',        # ← Exact cum returneaza detectorul
    'sad': 'sad',
    'angry': 'angry',
    'surprise': 'surprise',  # Nu 'surprised'!
    'neutral': 'neutral'
}

# Verifica ce returnează detectorul:
# Seteaza debug mode în app.py:
print(f"Emotion detected: {final_emotion}")
```

---

### 9. Noul fișier de imagine nu se încarcă

**Simptom:** După ce am adăugat o imagine nouă, nu apare

**Cauze:**
- Cache Python
- Fișier .pyc vechi

**Soluție:**
```bash
# 1. Șterge cache Python
find /home/neaguandrei05/tema_IA4/emotion-detecting-system -name "*.pyc" -delete
find /home/neaguandrei05/tema_IA4/emotion-detecting-system -name "__pycache__" -type d -delete

# 2. Restart Flask
# Ctrl+C pe terminal
# python3 app.py

# 3. Reîncarcă pagina browser (Ctrl+F5 hard refresh)
```

---

### 10. Alte emoții (nu doar 5) se detectează

**Simptom:** Detectorul returnează emoții care nu sunt în mapping

**Cauze:**
- Detectorul (Mediapipe/Tensorflow) returnează alte clase

**Soluție:**
```python
# Adauga logging în app.py:
print(f"DEBUG: Emotion from detector: {emotion}")
print(f"DEBUG: Mapped to: {EMOTION_FILENAMES.get(emotion, 'UNKNOWN')}")

# Daca sunt alte emoții, mapa-le:
EMOTION_FILENAMES = {
    'happy': 'happy',
    'sad': 'sad',
    'angry': 'angry',
    'surprise': 'surprise',
    'neutral': 'neutral',
    'disgust': 'angry',    # Map disgust to angry
    'fear': 'surprise'     # Map fear to surprise
}
```

---

## 🔍 Debug Mode

### Activează logging detaliat

```python
# În app.py, adaugă la început:
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Apoi adaugă în get_image_for_emotion():
print(f"[DEBUG] get_image_for_emotion({emotion}, {library_name})")
print(f"[DEBUG] Searched in: {library_path}")
```

### Monitorizează requesturi API

```javascript
// În main.js, adaugă la procesare:
fetch('/process_frame', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({image: imageData})
})
.then(r => r.json())
.then(data => {
    console.log('Response:', data);  // ← Afișează răspunsul complet
    updateUI(data);
});
```

---

## ✅ Checklist Diagnostic

Dacă imaginile nu funcționează, verifică:

- [ ] Folderele bibliotecilor există
- [ ] Fișierele imaginilor sunt în folderele corecte
- [ ] Denumirile fișierelor sunt lowercase
- [ ] Extensiile sunt acceptate (png, jpg, jpeg, gif, webp)
- [ ] Dicționarul LIBRARIES e actualizar în app.py
- [ ] Endpoint /get_libraries returnează bibliotheca corectă
- [ ] Consola browserului nu afișează erori 404
- [ ] Consola Flask nu afișează erori Python
- [ ] Calea returnată de backend e validă
- [ ] <img> elementul are ID corect: emotionImage

---

## 📞 Contact

Dacă problemele persistă, colectează:
1. Screenshot al erorii
2. Console log din browser (F12 > Console)
3. Terminal output de la Flask
4. Structura folderelor (`ls -la static/libraries/`)

---

**Ultima actualizare:** December 17, 2024  
**Versiune:** 1.0
