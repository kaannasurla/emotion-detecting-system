import os
import shutil
import random
import glob

# Configurare
SOURCE_DATA_DIR = 'raw_data'  # Puneți datasetul original aici (ex. raw_data/angry/image.jpg)
OUTPUT_DATA_DIR = 'data'      # Unde vor fi stocate datele împărțite
TRAIN_SPLIT = 0.8             # 80% pentru antrenare, 20% pentru testare

def split_dataset():
    if not os.path.exists(SOURCE_DATA_DIR):
        print(f"Eroare: Directorul sursă '{SOURCE_DATA_DIR}' nu a fost găsit.")
        print("Vă rugăm să creați un folder 'raw_data' și să puneți folderele cu emoții în el.")
        return

    # Creare directoare de ieșire
    train_dir = os.path.join(OUTPUT_DATA_DIR, 'train')
    test_dir = os.path.join(OUTPUT_DATA_DIR, 'test')
    
    # Verificare director de ieșire
    if os.path.exists(OUTPUT_DATA_DIR):
        response = input(f"Directorul de ieșire '{OUTPUT_DATA_DIR}' există deja. Suprascrie? (y/n): ")
        if response.lower() == 'y':
            shutil.rmtree(OUTPUT_DATA_DIR)
        else:
            print("Operațiune anulată.")
            return

    classes = [d for d in os.listdir(SOURCE_DATA_DIR) if os.path.isdir(os.path.join(SOURCE_DATA_DIR, d))]
    
    if not classes:
        print("Nu s-au găsit directoare de clasă în folderul sursă.")
        return

    print(f"Clase găsite: {classes}")

    for class_name in classes:
        print(f"Procesare {class_name}...")
        
        # Creare directoare clase în train/test
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)
        
        # Obținere toate imaginile
        source_class_path = os.path.join(SOURCE_DATA_DIR, class_name)
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            images.extend(glob.glob(os.path.join(source_class_path, ext)))
            
        random.shuffle(images)
        
        split_point = int(len(images) * TRAIN_SPLIT)
        train_images = images[:split_point]
        test_images = images[split_point:]
        
        # Copiere fișiere
        for img in train_images:
            shutil.copy(img, os.path.join(train_dir, class_name, os.path.basename(img)))
            
        for img in test_images:
            shutil.copy(img, os.path.join(test_dir, class_name, os.path.basename(img)))
            
        print(f"  - Train: {len(train_images)}")
        print(f"  - Test: {len(test_images)}")

    print("Data split complete.")

if __name__ == "__main__":
    split_dataset()
