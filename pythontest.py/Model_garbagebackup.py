import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import gc

# --- 1. SETUP CONSTANTS ---
# Kept at 8 to prevent "Relay Timeout" crashes on Colab
BATCH_SIZE = 8 
IMG_SIZE = (224, 224)
DATA_DIR = '/content/garbage_dataset'
CHECKPOINT_PATH = "/content/drive/MyDrive/garbage_checkpoints/model_checkpoint.keras"

# Create checkpoint directory if it doesn't exist
os.makedirs(os.path.dirname(CHECKPOINT_PATH), exist_ok=True)

# --- 2. LOAD DATA PIPELINE ---
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    interpolation='bilinear'
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    interpolation='bilinear'
)

# GET CLASS NAMES (Must be done before prefetching)
class_names = train_ds.class_names
num_classes = len(class_names)
print(f"✅ Classes found ({num_classes}): {class_names}")

# --- 3. PERFORMANCE ---
AUTOTUNE = tf.data.AUTOTUNE
# Shuffle buffer 200 is safer for RAM than 500
train_ds = train_ds.shuffle(200).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# --- 4. DATA AUGMENTATION ---
data_augmentation = keras.Sequential([
  layers.RandomFlip("horizontal"),
  layers.RandomRotation(0.1),
  layers.RandomZoom(0.1),
  layers.RandomContrast(0.1),
])

# --- 5. BUILD THE MODEL (Transfer Learning) ---
base_model = tf.keras.applications.EfficientNetB0(
    input_shape=IMG_SIZE + (3,),
    include_top=False, 
    weights='imagenet'
)
base_model.trainable = False

# Functional API Construction
inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = base_model(x, training=False) 
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x) 
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs, outputs)

# --- 6. COMPILE ---
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# --- 7. CHECKPOINT CALLBACK (Safety Net) ---
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=CHECKPOINT_PATH,
    save_best_only=True,
    monitor='val_accuracy',
    verbose=1
)

# --- 8. TRAIN (Phase 1) ---
# Clear RAM before starting
gc.collect()
tf.keras.backend.clear_session()

print("🚀 Starting Training (Phase 1)...")
epochs = 10
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[cp_callback]
)

# --- 9. FINE TUNING ---
print("🔧 Starting Fine-Tuning (Phase 2)...")
base_model.trainable = True
# Freeze the bottom layers, unfreeze the top 100
fine_tune_at = 100 
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

fine_tune_epochs = 10
total_epochs = epochs + fine_tune_epochs

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    initial_epoch=history.epoch[-1],
    epochs=total_epochs,
    callbacks=[cp_callback]
)

# --- 10. SAVE FINAL MODEL ---
final_save_path = '/content/drive/MyDrive/Garbage_classifier_Final.keras'
model.save(final_save_path)
print(f"✅ SUCCESS: Final model saved to {final_save_path}")