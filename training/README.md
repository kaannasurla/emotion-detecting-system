# Antrenarea pentru Detectarea Emoțiilor

Acest director conține scripturi pentru antrenarea modelului de detectare a emoțiilor.

## Fișiere

- `train.py`: Scriptul principal pentru antrenarea Rețelei Neurale Convoluționale (CNN).
- `split_data.py`: Un script utilitar pentru împărțirea unui set de date brut în seturi de antrenare și testare.

## Configurare

1.  **Instalare Dependențe**: Asigurați-vă că aveți instalate bibliotecile Python necesare.
    ```bash
    pip install opencv-python numpy pandas matplotlib scikit-learn tensorflow
    ```

2.  **Pregătirea Datelor**:
    -   Puneți imaginile setului de date brut într-un dosar numit `raw_data` în interiorul acestui director.
    -   Structura ar trebui să fie:
        ```
        raw_data/
            angry/
                image1.jpg
                ...
            happy/
                image2.jpg
                ...
            ...
        ```
    -   Rulați `python split_data.py` pentru a crea directorul `data/` cu împărțirile `train` și `test`.

## Antrenare

Rulați scriptul de antrenare:

```bash
python train.py
```

Argumentele sunt momentan hardcodate în `train.py` (de exemplu, `EPOCHS`, `BATCH_SIZE`). Le puteți modifica direct în secțiunea "Configuration" a scriptului.

## Rezultate

-   **Model**: Modelul antrenat va fi salvat în `../models/emotion_model.h5`.
-   **Istoric**: Un grafic al acurateței și pierderii (loss) antrenamentului va fi salvat ca `training_history.png`.
