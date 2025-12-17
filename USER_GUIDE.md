# 🎮 INSTRUCȚIUNI PENTRU UTILIZATOR

## ✨ Bine venit în Emotion Detecting System v1.0

Această aplicație detectează emoțiile tale în timp real folosind camera web și inteligență artificială!

---

## 🚀 PASUL 1: Pornire Aplicație

### Pe Linux/Mac:
```bash
cd /home/neaguandrei05/tema_IA4/emotion-detecting-system
python3 app.py
```

### Așteptă:
```
* Running on http://127.0.0.1:5000
```

### Deschide browser-ul:
- Accesează: **http://localhost:5000**

---

## 📷 PASUL 2: Acorda Permisiune la Cameră

Când accesezi site-ul:
1. Browser-ul va cere permisiune la cameră
2. Dă click pe "Allow" / "Permite"
3. Se va deschide feed-ul video

**IMPORTANT:** Dacă nu vezi feed video, verifică:
- [ ] Camera conectată la computer
- [ ] Permisiuni cameră acordate
- [ ] Nu sunt alte aplicații care folosesc camera

---

## 🎨 PASUL 3: Selectare Bibliotecă

La top vei vedea 3 butoane cu biblioteci:

### 🥊 **Clash Royale**
Imagini tematice din jocul Clash Royale
- Happy: Personaj fericit
- Sad: Personaj trist
- Angry: Personaj furios
- Surprise: Personaj surprins
- Neutral: Personaj neutru

### 🐵 **Monkey**
Imagini cute cu maimuțe
- Happy: Maimuță zâmbitoare
- Sad: Maimuță tristă
- Angry: Maimuță furioasă
- Surprise: Maimuță surprinsă
- Neutral: Maimuță neutră

### 🎤 **Florin Salam**
Imagini tematice cu Florin Salam
- Happy: Florin fericit
- Sad: Florin trist
- Angry: Florin furios
- Surprise: Florin surprins
- Neutral: Florin neutru

**Dă click pe oricare din butoane pentru a selecta o bibliotecă.**

---

## 😊 PASUL 4: Folosire Aplicație

### Cum funcționează:
1. **Fii în fața camerei** - Aplicația te va vedea
2. **Schimbă expresia** - Zâmbește, frunci sprâncenel, surprinde-te
3. **Imaginea se schimbă** - Pe măsură ce emoția se schimbă
4. **Vezi procentul** - Bară albastră = încredere a AI

### Indicatoare:
- 📊 **Bară progres** - Cât de sigur e AI (100% = foarte sigur)
- 🎨 **Culoare card** - Se schimbă cu emoția
- 🖼️ **Imagine** - Arată emoția detectată din biblioteca selectată

---

## 🎮 PASUL 5: Butoane Controale

### 🔄 **Detectează Emoția**
- Forțează o nouă detectare
- Util dacă schimbarea e lentă

### 📸 **Salvează Captură**
- Salvează o imagine din camera + emoția detectată
- Se salvează în folder: `static/captures/`
- Util pentru amintiri!

### 📊 **Istoric**
- Afișează grafic cu evoluția emoțiilor
- Util pentru a vedea cum s-a schimbat emoția în timp

### 🗑️ **Șterge Istoric**
- Curăță graficul și istoricul
- Util ca să restarezi

---

## 🔀 PASUL 6: Schimbarea Bibliotecilor

**Poți schimba biblioteca oricând**, și imaginile se vor actualiza imediat!

### Exemplu:
1. Selectezi 🥊 Clash Royale
2. Zâmbești → Apare imagine Clash Royale fericit
3. Click pe 🐵 Monkey
4. Imaginea se schimbă → Apare maimuță fericit
5. Frunci sprâncenel
6. Imaginea se schimbă → Apare maimuță furios
7. Etc...

**TIP:** Schimbă biblioteci pe parcursul utilizării pentru a vedea diferite reprezentări ale emoțiilor tale!

---

## ⚙️ OPȚIONAL: Selectare Model AI

Dacă sunt disponibile, poți alege modelul AI:
- **Mediapipe** - Mai rapid, mai ușor
- **Tensorflow** - Mai precis, mai greu

**Buton** va apărea la top dacă sunt ambele disponibile.

---

## 📱 ACCESSIBILITY

### Pe Telefon/Tablet:
Aplicația e responsive, deci funcționează și pe ecrane mici:
```
┌─────────────────┐
│ 📚 Biblioteci   │  ← Butoanele se aranjează vertical
│                 │
│ [📸 Video]      │  ← Video se redimensionează
│                 │
│ [Imagine]       │  ← Imaginea se redimensionează
│ Emoție          │
│ Progress bar    │
│                 │
│ [Butoane]       │  ← Butoanele se aranjează vertical
└─────────────────┘
```

### De pe calculator:
Funcționează perfect pe orice rezoluție de ecran.

---

## 🆘 TROUBLESHOOTING

### ❌ "Nu se conectează la cameră"
**Soluție:** 
- Verifica că ai acordat permisiuni
- Reîncarcă pagina (F5)
- Încearcă alt browser

### ❌ "Imaginile nu se afișează, doar emoji"
**Soluție:**
- Reîncarcă pagina (Ctrl+F5 hard refresh)
- Verifica că bibliotecile sunt selectate
- Vezi `TROUBLESHOOTING.md`

### ❌ "Emoția nu se detecează corect"
**Normal!** - AI nu e perfectă. Încearcă:
- Luz mai bună
- Fața mai clar vizibilă
- Expresii mai exagerate

### ❌ "Aplicația e lentă"
**Soluție:**
- Închide alte tab-uri
- Restart browser
- Verifica viteza internet

### ❌ "Alte probleme?"
- Citește: `TROUBLESHOOTING.md`
- Contactează: Developer

---

## 💡 SFATURI ȘI TRUCURI

### ✅ Pentru Cele Mai Bune Rezultate:

1. **Luminare Bună** - Asigură-te că fața e bine iluminată
2. **Fără Ochelari de Soare** - AI trebuie să vadă ochii
3. **Fără Cap Acoperit** - Fața trebuie clar vizibilă
4. **Expresii Exagerate** - Cu cât mai exagerat, cu atât mai bine
5. **Apropiat de Cameră** - 30-60cm distanță ideală

### 🎮 Pentru Distracție:

1. **Testează Expresii** - Incearcă să "fool" AI-ul
2. **Schimbă Rapid** - Vezi cât de repede reacționează
3. **Schimbă Biblioteci** - Vede cum se schimbă imaginea
4. **Salvează Capturi** - Fă-ți o colecție de expresii
5. **Compară cu Prietenul** - Vezi cine are expresiile mai "corecte"

---

## 📊 CITIRE REZULTATE

### Emoțiile detectate:
- 😊 **Happy** - Zâmbet, pomi relaxati
- 😢 **Sad** - Colt guri in jos, ochi tristi
- 😠 **Angry** - Frunci sprâncenel, buze apasate
- 😲 **Surprise** - Ochi larg deschiși, gura deschisa
- 😐 **Neutral** - Fata neutra, fara expresie clara

### Indicele de Încredere:
- 🟩 **90-100%** - SIGUR! AI-ul e foarte confident
- 🟨 **70-89%** - POSIBIL - AI-ul e destul de sigur
- 🟧 **50-69%** - INCERT - AI-ul e nesigur
- 🟥 **0-49%** - NEFIABIL - Ignora

---

## 🚪 IEȘIRE DIN APLICAȚIE

### Pentru a opri aplicația:
1. În browser: Închide tab-ul sau închiide browser-ul
2. În terminal: Apasă **Ctrl+C**
3. Await: `Keyboard Interrupt`

---

## 📝 NOTAȚII IMPORTANȚĂ

- ⚠️ **Cameră:** Necesară pentru funcționare
- ⚠️ **Lumină:** Important pentru acuratețe
- ⚠️ **Internet:** Nu e necesar (funcționează local)
- ⚠️ **CPU:** Poate folosi CPU (AI processing)

---

## 🎓 ÎNVAȚĂ MAI MULT

### Fișiere de referință:
- `QUICKSTART.md` - Start rapid
- `LIBRARIES_README.md` - Cum să adaugi biblioteci
- `TROUBLESHOOTING.md` - Rezolvare probleme
- `FINAL_REPORT.md` - Detalii tehnice

---

## 🎉 DIVERȚIE!

Acum ești gata să te distrezi cu Emotion Detecting System!

### Ideile de activități:
1. ✅ Test expresiile tale
2. ✅ Schimbă rapid între emoții
3. ✅ Salvează cele mai bune capturi
4. ✅ Compară cu prietenii
5. ✅ Fă-ți o colecție de imagini
6. ✅ Vede cât de bun e AI-ul

---

## 📞 FEEDBACK

Dacă au o idee, sugestie sau problemă:
1. Verifica `TROUBLESHOOTING.md`
2. Citește `FINAL_REPORT.md`
3. Contactează developer

---

**Versiune:** 1.0  
**Data:** December 17, 2024  
**Status:** ✅ Ready to Use

---

## 🌟 ȘI CAM ATÂT!

**Enjoy! 🚀✨**

Ai o aplicație modernă care detectează emoții în timp real și le afișează cu imagini dintr-o bibliotecă pe care o poți alege!

**Happy emotions! 😊**
