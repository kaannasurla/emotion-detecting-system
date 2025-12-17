import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Configurare
IMG_SIZE = 48
BATCH_SIZE = 64
EPOCHS = 50
LEARNING_RATE = 0.001
DATA_DIR = 'data'  # Structura așteptată: data/train/nume_clasă și data/test/nume_clasă
MODEL_PATH = '../models/emotion_model.h5'

# Verificare existență director date
if not os.path.exists(DATA_DIR):
    print(f"Eroare: Directorul de date '{DATA_DIR}' nu a fost găsit.")
    print("Vă rugăm să descărcați un dataset (ex. FER-2013) și să îl extrageți aici.")
    print("Structura așteptată:")
    print(f"  {DATA_DIR}/train/angry/...")
    print(f"  {DATA_DIR}/train/happy/...")
    print("  etc.")
    exit(1)

# Generatoare
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

print("Încărcare date...")
try:
    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'train'),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        shuffle=True
    )

    validation_generator = val_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'test'), # Adesea numit 'test' sau 'validation' în dataseturile Kaggle
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        shuffle=False
    )
except Exception as e:
    print(f"Eroare la încărcarea datelor: {e}")
    print("Asigurați-vă că aveți subdirectoarele 'train' și 'test' în 'data/'.")
    exit(1)

# Definire Model
# Bazat pe arhitectură stil VGG simplificată
def build_model(num_classes):
    model = Sequential()
    
    # Bloc 1
    model.add(Input(shape=(IMG_SIZE, IMG_SIZE, 1)))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # Bloc 2
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # Bloc 3
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # Strat Dens
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    
    model.add(Dense(num_classes, activation='softmax'))

    return model

num_classes = train_generator.num_classes
class_names = list(train_generator.class_indices.keys())
print(f"Clase detectate: {class_names}")

model = build_model(num_classes)

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Callback-uri
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    verbose=1,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    verbose=1,
    min_lr=1e-6
)

# Antrenare
print("Pornire antrenare...")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[checkpoint, early_stopping, reduce_lr]
)

# Grafice
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Acuratețe Antrenare')
plt.plot(history.history['val_accuracy'], label='Acuratețe Validare')
plt.legend()
plt.title('Acuratețe')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Pierdere Antrenare')
plt.plot(history.history['val_loss'], label='Pierdere Validare')
plt.legend()
plt.title('Pierdere')
plt.savefig('training_history.png')
print("Istoricul antrenării salvat în training_history.png")

# Evaluare
print("Evaluare model...")
predictions = model.predict(validation_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = validation_generator.classes

print("\nConfusion Matrix:")
cm = confusion_matrix(y_true, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))

print(f"\nModel saved to {os.path.abspath(MODEL_PATH)}")
