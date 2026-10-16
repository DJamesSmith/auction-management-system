import os
import json
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications.resnet50 import preprocess_input


# ============================================================
# 1. MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "..", "models", "fashion_model.keras"
)

CLASS_PATH = os.path.join(
    BASE_DIR, "..", "models", "class_names.json"
)


# ============================================================
# 2. LOAD MODEL AND CLASS NAMES
# ============================================================

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as file:
    class_names = json.load(file)

print("Fashion MNIST model loaded successfully.")
print("Number of categories:", len(class_names))


# ============================================================
# 3. PREPROCESS IMAGE
# ============================================================

def preprocess_fashion_image(image_path):

    # Read uploaded image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read the uploaded image.")

    # Convert BGR to grayscale
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Resize to Fashion MNIST dimensions
    image = cv2.resize(
        image,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )

    # Convert grayscale to RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_GRAY2RGB
    )

    # Resize to the ResNet50 input size used during training
    image = cv2.resize(
        image,
        (96, 96),
        interpolation=cv2.INTER_LINEAR
    )

    # Convert to float32
    image = image.astype(np.float32)

    # Apply the same ResNet50 preprocessing as training
    image = preprocess_input(image)

    # Add batch dimension: (1, 96, 96, 3)
    image = np.expand_dims(image, axis=0)

    return image


# ============================================================
# 4. PREDICT CATEGORY
# ============================================================

def get_predicted_class(image):

    prediction = model.predict(image, verbose=0)

    predicted_class = int(np.argmax(prediction[0]))

    confidence = float(np.max(prediction[0]))

    print("Prediction probabilities:", prediction[0])
    print("Predicted class index:", predicted_class)
    print("Confidence:", confidence)

    return predicted_class, confidence


# ============================================================
# 5. GET CATEGORY NAME
# ============================================================

def get_fashion_category(predicted_class):

    if predicted_class < 0 or predicted_class >= len(class_names):
        return "Unknown Category"

    return class_names[predicted_class]


# ============================================================
# 6. FORMAT CATEGORY NAME
# ============================================================

def format_category_name(category_name):

    category_name = category_name.replace("_", " ")

    category_name = " ".join(category_name.split())

    return category_name.title()


# ============================================================
# 7. COMPLETE PREDICTION FUNCTION
# ============================================================

def predict_auction_category(image_path):

    processed_image = preprocess_fashion_image(image_path)

    predicted_class, confidence = get_predicted_class(
        processed_image
    )

    category_name = get_fashion_category(predicted_class)

    formatted_category = format_category_name(category_name)

    return {
        "category": formatted_category,
        "confidence": round(confidence * 100, 2)
    }