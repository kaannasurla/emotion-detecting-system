# 📚 Emotion Detecting System - Biblioteci de Imagini

## Descriere

Aplicația suportă acum **multiple biblioteci de imagini** pentru a afișa reprezentări vizuale ale emoțiilor detectate, în loc de emoji-uri. Utilizatorul poate alege între diferite teme/biblioteci.

## Biblioteci Disponibile

### 1. 👑 Clash Royale
- Imagini tematice din jocul Clash Royale
- Fișiere: `happy.jpg`, `sad.jpg`, `angry.png`, `surprise.png`, `neutral.webp`
- Locație: `static/libraries/clash_royale/`

### 2. 🐵 Monkey
- Imagini cu maimuțe pentru fiecare stare emoțională
- Fișiere: `happy.jpg`, `sad.gif`, `angry.jpg`, `surprise.png`, `neutral.webp`
- Locație: `static/libraries/monkey/`

### 3. 🎤 Florin Salam
- Imagini tematice cu Florin Salam
- Fișiere: `happy.jpg`, `sad.jpg`, `angry.png`, `surprise.webp`, `neutral.jpg`
- Locație: `static/libraries/florin_salam/`

## Cum să Adaugi o Nouă Bibliotecă

### Pasul 1: Creează un folder
```bash
mkdir -p static/libraries/nume_biblioteca/
```

### Pasul 2: Adaugă imagini
Denumește imaginile conform emoțiilor detectate:
- `happy.[ext]` - pentru emoția "happy" (fericit)
- `sad.[ext]` - pentru emoția "sad" (trist)
- `angry.[ext]` - pentru emoția "angry" (furios)
- `surprise.[ext]` - pentru emoția "surprise" (surprins)
- `neutral.[ext]` - pentru emoția "neutral" (neutru)

**Extensii acceptate:** `png`, `jpg`, `jpeg`, `gif`, `webp`

Exemplu:
```bash
static/libraries/nume_biblioteca/
├── happy.jpg
├── sad.png
├── angry.jpg
├── surprise.png
└── neutral.webp
```

### Pasul 3: Update `app.py`
Adaugă biblioteca în dicționarul `LIBRARIES`:

```python
LIBRARIES = {
    'clash_royale': 'static/libraries/clash_royale',
    'monkey': 'static/libraries/monkey',
    'florin_salam': 'static/libraries/florin_salam',
    'nume_biblioteca': 'static/libraries/nume_biblioteca'  # ← Noua bibliotecă
}
```

### Pasul 4: Restart aplicația
```bash
python3 app.py
```

Noua bibliotecă va apărea automat în interfață la alegere!

## Cum Funcționează

1. Utilizatorul selectează o bibliotecă de imagini din meniu
2. La detectarea unei emoții, aplicația caută imaginea corespunzătoare din biblioteca selectată
3. Imaginea se afișează în centru, înlocuind emoji-ul
4. Dacă imaginea nu este găsită, se afișează emoji-ul fallback

## Detalii Tehnice

### Mapping Emoții
```python
EMOTION_FILENAMES = {
    'happy': 'happy',
    'sad': 'sad',
    'angry': 'angry',
    'surprise': 'surprise',
    'neutral': 'neutral'
}
```

### Calea Imaginilor
- Aplicația caută imaginile în ordinea extensiilor: `png`, `jpg`, `jpeg`, `gif`, `webp`
- Returnează calea relativă: `/static/libraries/library_name/emotion.ext`

### Endpoint API
- `GET /get_libraries` - Obține lista bibliotecilor disponibile
- `POST /switch_library` - Schimbă biblioteca activă
- Body: `{"library": "library_name"}`

## Sfaturi

- 📐 **Rezoluție recomandată:** 200x200px sau mai mare
- 🎨 **Format recomandat:** PNG (transparent) sau JPG (culori pline)
- 📦 **Mărime fișier:** Sub 500KB per imagine
- 🎯 **Aspect ratio:** Pătrat (1:1) pentru cea mai bună afișare

## Suport

Dacă imginele nu se afișează:
1. Verifică consola browserului (F12 > Console)
2. Asigură-te că folderele și fișierele au permisiunile corecte
3. Verifică că extensiile sunt în lista acceptate
4. Redeschide aplicația după adăugarea noilor fișiere

---

**Versiune:** 1.0  
**Ultima actualizare:** December 17, 2024
