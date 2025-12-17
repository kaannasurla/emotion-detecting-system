# 📚 QUICK START - Sistemul de Biblioteci de Imagini

## 🚀 Cum să pornești aplicația

```bash
cd /home/neaguandrei05/tema_IA4/emotion-detecting-system
python3 app.py
```

Accesează: **http://localhost:5000**

---

## 📖 Ce vei vedea

```
┌─────────────────────────────────────────────┐
│    🎭 Emotion Detecting System             │
│    Detectare emoții în timp real folosind AI│
├─────────────────────────────────────────────┤
│                                             │
│   📚 Selectează Biblioteca de Imagini:      │
│   [🥊Clash Royale] [🐵 Monkey] [🎤 Salam] │
│                                             │
│        [  Camera Feed Here  ]               │
│                                             │
│              [IMAGINE EMOȚIE]               │
│              Fericit                        │
│              ████████░░ 92%                 │
│                                             │
│   [🔄 Detectează] [📸 Salvează] [📊Info]  │
│                                             │
│        Grafic Istoric (ascuns)              │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎮 Cum să folosești

### 1️⃣ Selectează Biblioteca
Dă click pe una din butoanele bibliotecii:
- 🥊 **Clash Royale** - Imagini game Clash Royale
- 🐵 **Monkey** - Imagini cu maimuțe
- 🎤 **Florin Salam** - Imagini tematice

### 2️⃣ Apare în Cameră
Sistemul va detecta expresia ta și va afișa:
- ✅ O imagine din biblioteca selectată
- ✅ Percentaj de încredere
- ✅ Culoare în funcție de emoție

### 3️⃣ Schimbă Biblioteca pe Parcurs
Poți schimba biblioteca oricând - imaginile se vor actualiza instant!

---

## 🎨 Biblioteci de Imagini

### 📁 Clash Royale
```
static/libraries/clash_royale/
├── happy.jpg      (30 KB)   👑
├── sad.jpg        (48 KB)   👑
├── angry.png      (152 KB)  👑
├── surprise.png   (30 KB)   👑
└── neutral.webp   (15 KB)   👑
```

### 📁 Monkey
```
static/libraries/monkey/
├── happy.jpg      (5 KB)    🐵
├── sad.gif        (14 KB)   🐵
├── angry.jpg      (53 KB)   🐵
├── surprise.png   (163 KB)  🐵
└── neutral.webp   (40 KB)   🐵
```

### 📁 Florin Salam
```
static/libraries/florin_salam/
├── happy.jpg      (287 KB)  🎤
├── sad.jpg        (51 KB)   🎤
├── angry.png      (421 KB)  🎤
├── surprise.webp  (59 KB)   🎤
└── neutral.jpg    (32 KB)   🎤
```

---

## 🔌 API Endpoints

```
GET /get_libraries
→ {"libraries":["clash_royale","monkey","florin_salam"],"current":"clash_royale"}

POST /switch_library
→ {"library":"monkey"}
← {"success":true,"library":"monkey"}

POST /process_frame
→ {"image":"base64..."}
← {"emotion":"happy","confidence":0.92,"image":"/static/libraries/monkey/happy.jpg"}

GET /get_models
→ {"models":["mediapipe","tensorflow"],"current":"mediapipe"}
```

---

## 💡 Sfaturi

✅ **CE FUNCȚIONEAZĂ BINE:**
- Schimb rapid între biblioteci
- Detectare rapidă de emoții
- Fallback la emoji dacă imagine lipsește
- Salvare capturi cu emoții

⚠️ **OPTIMIZĂRI VIITOARE:**
- Mai multe formule de detectare
- Animații la schimb imagini
- Preload imagini pentru viteză
- Suport PNG transparent

---

## 🆘 Dacă Ceva Nu Merge

1. **Deschide DevTools:** F12
2. **Check Console:** Caută erori roșii
3. **Verifica Network:** Caută errori 404
4. **Verifică Terminal:** Cauta erori Flask

**Citește:** `TROUBLESHOOTING.md` pentru soluții detaliate

---

## 📝 Pentru Developeri

### Adaugă Nouă Bibliotecă

```bash
# 1. Crează folder
mkdir static/libraries/Disney

# 2. Adaugă 5 imagini
cp poza1.jpg static/libraries/Disney/happy.jpg
cp poza2.jpg static/libraries/Disney/sad.jpg
# ... etc

# 3. Editează app.py
LIBRARIES = {
    'clash_royale': 'static/libraries/clash_royale',
    'monkey': 'static/libraries/monkey',
    'florin_salam': 'static/libraries/florin_salam',
    'disney': 'static/libraries/Disney'  # ← NOUA
}

# 4. Restart
python3 app.py
```

### Verifica Statusul

```bash
python3 test_libraries.py
# Afișează status complet
```

---

## 📊 Comparație cu Versiunea Veche

| Feature | Veche (Emoji) | Nouă (Imagini) |
|---------|---------------|----------------|
| Afișare emoții | 😊😢😠😲😐 | 🖼️ Imagini |
| Biblioteci | 0 | 3 (extensibil) |
| Personalizare | 0 | ✅ Alta |
| Schimb rapid | ❌ | ✅ |
| API endpoints | 5 | 7 |
| Coduri linii | ~250 | ~350 |

---

## 🎯 Fluxul Complet

```
┌──────────────────┐
│ User deschide    │
│ aplicația        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ loadLibraries()  │
│ → GET /libs      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Se afișează      │
│ 3 butoane        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ User pe buton    │
│ Monkey           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ switchLibrary()  │
│ → POST /libs     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Backend update   │
│ current_library  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ processFrame()   │
│ detectează       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ get_image_for... │
│ → cauta imagine  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Returnează path  │
│ /static/lib/...  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ updateUI()       │
│ afișează imagine │
└──────────────────┘
```

---

## 📞 Contact & Support

- 📖 Documentație completă: `LIBRARIES_README.md`
- 🔧 Troubleshooting: `TROUBLESHOOTING.md`
- 📋 Schimbări: `CHANGES.md`
- 🧪 Test: `test_libraries.py`

---

**Ediție:** v1.0  
**Data:** December 17, 2024  
**Status:** ✅ Gata de producție
