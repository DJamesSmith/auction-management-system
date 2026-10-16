import os
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


# ============================================================
# 1. CHECK TENSORFLOW AND GPU
# ============================================================

print("TensorFlow version:", tf.__version__)
print("GPU:", tf.config.list_physical_devices("GPU"))

SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)


# ============================================================
# 2. SETTINGS
# ============================================================

IMAGE_SIZE = (96, 96)
BATCH_SIZE = 64
EPOCHS = 10
AUTOTUNE = tf.data.AUTOTUNE


# ============================================================
# 3. LOAD FASHION MNIST DATASET
# ============================================================

(x_train_all, y_train_all), (x_test, y_test) = (tf.keras.datasets.fashion_mnist.load_data())

print("\nTraining images:", x_train_all.shape)
print("Training labels:", y_train_all.shape)
print("Test images:", x_test.shape)
print("Test labels:", y_test.shape)


# ============================================================
# 4. CLASS NAMES
# ============================================================

class_names = ["T-shirt/top","Trouser","Pullover","Dress","Coat","Sandal","Shirt","Sneaker","Bag","Ankle boot"]
NUM_CLASSES = len(class_names)

print("\nClass mapping:")
for i, name in enumerate(class_names):
    print(i, "->", name)


# ============================================================
# 5. DISPLAY ORIGINAL DATASET IMAGES
# ============================================================

plt.figure(figsize=(12, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_train_all[i], cmap="gray")
    plt.title(class_names[int(y_train_all[i])])
    plt.axis("off")

plt.tight_layout()
plt.show()


# ============================================================
# 6. CREATE TRAINING AND VALIDATION SETS
# ============================================================

x_train, x_val, y_train, y_val = train_test_split(x_train_all,y_train_all,test_size=0.15,random_state=SEED,stratify=y_train_all)

print("\nTraining samples:", len(x_train))
print("Validation samples:", len(x_val))
print("Test samples:", len(x_test))


# ============================================================
# 7. PREPROCESS IMAGES FOR RESNET50
# ============================================================

def preprocess_image(image, label):
    # Convert grayscale [28, 28] to [28, 28, 1]
    image = tf.expand_dims(image, axis=-1)

    # Convert grayscale to RGB [28, 28, 3]
    image = tf.image.grayscale_to_rgb(image)

    # Resize to the input size used by our model
    image = tf.image.resize(image, IMAGE_SIZE)

    # Apply ResNet50-specific preprocessing
    image = preprocess_input(image)

    return image, label


# ============================================================
# 8. CREATE TF.DATA PIPELINES
# ============================================================

def create_dataset(images, labels, training=False):
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))

    if training:
        dataset = dataset.shuffle(buffer_size=len(images),seed=SEED)

    dataset = dataset.map(preprocess_image,num_parallel_calls=AUTOTUNE)

    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(AUTOTUNE)

    return dataset


train_ds = create_dataset(x_train, y_train, training=True)
val_ds = create_dataset(x_val, y_val)
test_ds = create_dataset(x_test, y_test)

print("\nDatasets prepared successfully.")


# ============================================================
# 9. LOAD PRETRAINED RESNET50
# ============================================================

base_model = ResNet50(weights="imagenet",include_top=False,input_shape=(96, 96, 3))


# ============================================================
# 10. FREEZE RESNET50 LAYERS
# ============================================================

base_model.trainable = False


# ============================================================
# 11. BUILD CLASSIFICATION MODEL
# ============================================================

inputs = tf.keras.Input(shape=(96, 96, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(NUM_CLASSES,activation="softmax")(x)
model = tf.keras.Model(inputs=inputs,outputs=outputs)


# ============================================================
# 12. COMPILE MODEL
# ============================================================

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# ============================================================
# 13. TRAIN MODEL
# ============================================================

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        "/kaggle/working/fashion_best.keras",
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
]

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)


# ============================================================
# 14. LOAD BEST MODEL
# ============================================================

model = tf.keras.models.load_model("/kaggle/working/fashion_best.keras")


# ============================================================
# 15. PLOT TRAINING ACCURACY AND LOSS
# ============================================================

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Training")
plt.plot(history.history["val_accuracy"], label="Validation")
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Training")
plt.plot(history.history["val_loss"], label="Validation")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# 16. TEST MODEL
# ============================================================

test_loss, test_accuracy = model.evaluate(test_ds,verbose=1)

print("\n========== TEST RESULTS ==========")
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")


# ============================================================
# 17. CLASSIFICATION REPORT
# ============================================================

y_prob = model.predict(test_ds, verbose=1)
y_pred = np.argmax(y_prob, axis=1)

print("\n========== CLASSIFICATION REPORT ==========")

print(classification_report(
    y_test,
    y_pred,
    labels=list(range(NUM_CLASSES)),
    target_names=class_names,
    zero_division=0
))


# ============================================================
# 18. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(y_test,y_pred,labels=list(range(NUM_CLASSES)))

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(10, 8))

plt.imshow(cm, cmap="Blues")
plt.colorbar()

plt.xticks(range(NUM_CLASSES), class_names, rotation=45, ha="right")
plt.yticks(range(NUM_CLASSES), class_names)

plt.xlabel("Predicted Category")
plt.ylabel("Actual Category")
plt.title("Fashion MNIST Confusion Matrix")
plt.tight_layout()
plt.show()


# ============================================================
# 19. PREDICT ONE TEST IMAGE
# ============================================================

def predict_fashion_image(image, actual_label=None):

    # Accept an original 28x28 grayscale image.
    image = tf.convert_to_tensor(image, dtype=tf.float32)

    image = tf.expand_dims(image, axis=-1)
    image = tf.image.grayscale_to_rgb(image)
    image = tf.image.resize(image, IMAGE_SIZE)

    image = preprocess_input(image)
    image = tf.expand_dims(image, axis=0)

    probabilities = model.predict(image, verbose=0)[0]

    predicted_index = int(np.argmax(probabilities))
    predicted_name = class_names[predicted_index]
    confidence = float(probabilities[predicted_index]) * 100

    print("\nPredicted category:", predicted_name)
    print(f"Confidence: {confidence:.2f}%")

    if actual_label is not None:
        actual_name = class_names[int(actual_label)]
        print("Actual category:", actual_name)
        print(
            "Result:",
            "CORRECT" if predicted_index == int(actual_label)
            else "INCORRECT"
        )

    return predicted_name, confidence


# ============================================================
# 20. EXTRA TEST: RANDOM TEST IMAGES
# ============================================================

correct = 0
sample_count = 10

random_indices = np.random.default_rng(SEED).choice(
    len(x_test),
    size=sample_count,
    replace=False
)

plt.figure(figsize=(14, 8))

for position, index in enumerate(random_indices):

    image = x_test[index]
    actual_label = int(y_test[index])

    predicted_name, confidence = predict_fashion_image(
        image,
        actual_label
    )

    if predicted_name == class_names[actual_label]:
        correct += 1

    plt.subplot(2, 5, position + 1)
    plt.imshow(image, cmap="gray")
    plt.title(
        f"Pred: {predicted_name}\n"
        f"Actual: {class_names[actual_label]}"
    )
    plt.axis("off")

plt.tight_layout()
plt.show()

print("\n========== EXTRA TEST SUMMARY ==========")
print("Images tested:", sample_count)
print("Correct predictions:", correct)
print("Incorrect predictions:", sample_count - correct)
print(f"Sample accuracy: {correct / sample_count * 100:.2f}%")


# ============================================================
# 21. SAVE FINAL MODEL
# ============================================================

MODEL_PATH = "/kaggle/working/fashion_model.keras"

model.save(MODEL_PATH)

print("\nModel saved at:")
print(MODEL_PATH)


# ============================================================
# 22. SAVE CLASS NAMES
# ============================================================

CLASS_NAMES_PATH = "/kaggle/working/class_names.json"

with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(class_names, f, indent=4)

print("\nClass names saved at:")
print(CLASS_NAMES_PATH)


# ============================================================
# 23. VERIFY SAVED MODEL
# ============================================================

loaded_model = tf.keras.models.load_model(MODEL_PATH)

test_image = x_test[0]

# Prepare the image exactly as during inference
image = tf.convert_to_tensor(test_image, dtype=tf.float32)
image = tf.expand_dims(image, axis=-1)
image = tf.image.grayscale_to_rgb(image)
image = tf.image.resize(image, IMAGE_SIZE)
image = preprocess_input(image)
image = tf.expand_dims(image, axis=0)

original_prediction = model.predict(image, verbose=0)
loaded_prediction = loaded_model.predict(image, verbose=0)

print("\nSaved model verification:")

if np.allclose(
    original_prediction,
    loaded_prediction,
    atol=1e-5
):
    print("PASSED: Saved model predictions match.")
else:
    print("FAILED: Saved model predictions do not match.")


# ============================================================
# 24. CHECK GENERATED FILES
# ============================================================

print("\nFiles generated in /kaggle/working:")

for file in os.listdir("/kaggle/working"):
    print(file)