#!/usr/bin/env python3
"""
Script de test pentru a verifica dacă sistemul de biblioteci de imagini funcționează corect
"""

import os
import sys

# Adaugă calea proiectului
sys.path.insert(0, '/home/neaguandrei05/tema_IA4/emotion-detecting-system')

print("=" * 60)
print("🧪 TEST: Sistemul de Biblioteci de Imagini")
print("=" * 60)

# 1. Verifică structura folderelor
print("\n✅ PASUL 1: Verificare Structură Foldere")
print("-" * 60)

libraries_base = '/home/neaguandrei05/tema_IA4/emotion-detecting-system/static/libraries'
required_emotions = ['happy', 'sad', 'angry', 'surprise', 'neutral']

libraries = {
    'clash_royale': libraries_base + '/clash_royale',
    'monkey': libraries_base + '/monkey',
    'florin_salam': libraries_base + '/florin_salam'
}

all_good = True

for lib_name, lib_path in libraries.items():
    print(f"\n📚 Biblioteca: {lib_name}")
    
    if not os.path.exists(lib_path):
        print(f"  ❌ Folder nu există: {lib_path}")
        all_good = False
        continue
    
    files = os.listdir(lib_path)
    print(f"  ✓ Folder există")
    print(f"  ✓ Fișiere: {', '.join(sorted(files))}")
    
    # Verifica daca exista cel putin o imagine per emotie
    found_emotions = set()
    for emotion in required_emotions:
        for f in files:
            if emotion in f.lower():
                found_emotions.add(emotion)
                break
    
    missing = set(required_emotions) - found_emotions
    if missing:
        print(f"  ⚠️  Emoții lipsă: {', '.join(missing)}")
        all_good = False
    else:
        print(f"  ✓ Toate emoțiile sunt prezente")

# 2. Verifică codul Python
print("\n\n✅ PASUL 2: Verificare Cod Python")
print("-" * 60)

try:
    from app import LIBRARIES, EMOTION_FILENAMES, get_image_for_emotion
    print("✓ Import module Flask successful")
    print(f"✓ LIBRARIES definit: {list(LIBRARIES.keys())}")
    print(f"✓ EMOTION_FILENAMES definit: {list(EMOTION_FILENAMES.keys())}")
    
    # Test functie get_image_for_emotion
    print("\n🔍 Test get_image_for_emotion():")
    for lib in LIBRARIES.keys():
        for emotion in EMOTION_FILENAMES.keys():
            result = get_image_for_emotion(emotion, lib)
            if result:
                print(f"  ✓ {lib}: {emotion} → {result}")
            else:
                print(f"  ⚠️  {lib}: {emotion} → NOT FOUND")
    
except Exception as e:
    print(f"❌ Eroare la import: {e}")
    all_good = False

# 3. Verifică HTML și CSS
print("\n\n✅ PASUL 3: Verificare Fișiere Frontend")
print("-" * 60)

frontend_files = [
    '/home/neaguandrei05/tema_IA4/emotion-detecting-system/templates/index.html',
    '/home/neaguandrei05/tema_IA4/emotion-detecting-system/static/css/style.css',
    '/home/neaguandrei05/tema_IA4/emotion-detecting-system/static/js/main.js'
]

for fpath in frontend_files:
    fname = os.path.basename(fpath)
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f"✓ {fname} ({size} bytes)")
    else:
        print(f"❌ {fname} NU GĂSIT")
        all_good = False

# Verifică dacă au fost modificate pentru imagini
print("\n🔍 Verificare Modificări Frontend:")

try:
    with open('/home/neaguandrei05/tema_IA4/emotion-detecting-system/templates/index.html', 'r') as f:
        html_content = f.read()
        if 'emotionImageDisplay' in html_content:
            print("✓ HTML: Găsit emotionImageDisplay")
        else:
            print("❌ HTML: emotionImageDisplay NU GĂSIT")
        
        if 'libraryButtons' in html_content:
            print("✓ HTML: Găsit libraryButtons")
        else:
            print("❌ HTML: libraryButtons NU GĂSIT")
    
    with open('/home/neaguandrei05/tema_IA4/emotion-detecting-system/static/css/style.css', 'r') as f:
        css_content = f.read()
        if 'library-btn' in css_content:
            print("✓ CSS: Găsit library-btn styles")
        else:
            print("❌ CSS: library-btn styles NU GĂSITE")
        
        if 'emotion-image-display' in css_content:
            print("✓ CSS: Găsit emotion-image-display styles")
        else:
            print("❌ CSS: emotion-image-display styles NU GĂSITE")
    
    with open('/home/neaguandrei05/tema_IA4/emotion-detecting-system/static/js/main.js', 'r') as f:
        js_content = f.read()
        if 'loadLibraries' in js_content:
            print("✓ JS: Găsit loadLibraries()")
        else:
            print("❌ JS: loadLibraries() NU GĂSIT")
        
        if 'switchLibrary' in js_content:
            print("✓ JS: Găsit switchLibrary()")
        else:
            print("❌ JS: switchLibrary() NU GĂSIT")

except Exception as e:
    print(f"❌ Eroare la verificare frontend: {e}")
    all_good = False

# Rezultat final
print("\n" + "=" * 60)
if all_good:
    print("✅ TOATE TESTELE AU TRECUT!")
    print("Sistemul de biblioteci de imagini este gata de utilizare.")
else:
    print("⚠️  UNELE TESTE AU EȘUAT")
    print("Verifică erorile de mai sus.")
print("=" * 60)

sys.exit(0 if all_good else 1)
