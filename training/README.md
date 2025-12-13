# Emotion Detection Training

This directory contains scripts to train the emotion detection model.

## Files

- `train.py`: The main script to train the Convolutional Neural Network (CNN).
- `split_data.py`: A utility script to split a raw dataset into training and testing sets.

## Setup

1.  **Install Dependencies**: Ensure you have the necessary Python libraries installed.
    ```bash
    pip install opencv-python numpy pandas matplotlib scikit-learn tensorflow
    ```

2.  **Prepare Data**:
    -   Place your raw dataset images in a folder named `raw_data` inside this directory.
    -   The structure should be:
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
    -   Run `python split_data.py` to create the `data/` directory with `train` and `test` splits.

## Training

Run the training script:

```bash
python train.py
```

Arguments are currently hardcoded in `train.py` (e.g., `EPOCHS`, `BATCH_SIZE`). You can modify them directly in the "Configuration" section of the script.

## Output

-   **Model**: The trained model will be saved to `../models/emotion_model.h5`.
-   **History**: A plot of the training accuracy and loss will be saved as `training_history.png`.
