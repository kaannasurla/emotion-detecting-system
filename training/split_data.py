import os
import shutil
import random
import glob

# Configuration
SOURCE_DATA_DIR = 'raw_data'  # Put your original dataset here (e.g. raw_data/angry/image.jpg)
OUTPUT_DATA_DIR = 'data'      # Where the split data will go
TRAIN_SPLIT = 0.8             # 80% for training, 20% for testing

def split_dataset():
    if not os.path.exists(SOURCE_DATA_DIR):
        print(f"Error: Source directory '{SOURCE_DATA_DIR}' not found.")
        print("Please create a 'raw_data' folder and put your emotion folders inside it.")
        return

    # Create output directories
    train_dir = os.path.join(OUTPUT_DATA_DIR, 'train')
    test_dir = os.path.join(OUTPUT_DATA_DIR, 'test')
    
    # Check for output dir
    if os.path.exists(OUTPUT_DATA_DIR):
        response = input(f"Output directory '{OUTPUT_DATA_DIR}' already exists. Overwrite? (y/n): ")
        if response.lower() == 'y':
            shutil.rmtree(OUTPUT_DATA_DIR)
        else:
            print("Operation cancelled.")
            return

    classes = [d for d in os.listdir(SOURCE_DATA_DIR) if os.path.isdir(os.path.join(SOURCE_DATA_DIR, d))]
    
    if not classes:
        print("No class directories found in source folder.")
        return

    print(f"Found classes: {classes}")

    for class_name in classes:
        print(f"Processing {class_name}...")
        
        # Create class directories in train/test
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)
        
        # Get all images
        source_class_path = os.path.join(SOURCE_DATA_DIR, class_name)
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            images.extend(glob.glob(os.path.join(source_class_path, ext)))
            
        random.shuffle(images)
        
        split_point = int(len(images) * TRAIN_SPLIT)
        train_images = images[:split_point]
        test_images = images[split_point:]
        
        # Copy files
        for img in train_images:
            shutil.copy(img, os.path.join(train_dir, class_name, os.path.basename(img)))
            
        for img in test_images:
            shutil.copy(img, os.path.join(test_dir, class_name, os.path.basename(img)))
            
        print(f"  - Train: {len(train_images)}")
        print(f"  - Test: {len(test_images)}")

    print("Data split complete.")

if __name__ == "__main__":
    split_dataset()
