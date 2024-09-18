import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.mixed_precision import set_global_policy
import tensorflow as tf

# Enable mixed precision for faster training
set_global_policy('mixed_float16')

# Define paths
base_dir = 'E:/private_projects/mri-tumor-analysis/backend/Tumor'

# Image data generator for normalization and augmentation
datagen = ImageDataGenerator(
    rescale=1./255, 
    validation_split=0.2
)

# Load training data
train_generator = datagen.flow_from_directory(
    base_dir,  
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',  
    subset='training',
    shuffle=True  
)

# Load validation data
validation_generator = datagen.flow_from_directory(
    base_dir,  
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',  
    subset='validation'
)

# Model architecture
input_shape = (224, 224, 3)
num_classes = len(train_generator.class_indices)

model = Sequential()

# First block
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Second block
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Third block
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Fully connected layers
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# Optimizer and compile the model (use mixed precision)
optimizer = Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

# Callbacks for learning rate reduction and model checkpoint
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience=4, verbose=1, factor=0.5, min_lr=0.00001)
checkpoint_callback = ModelCheckpoint("new_model_saved", monitor='val_accuracy', save_best_only=True, mode='max')

# Model summary
model.summary()

# Train the model with reduced memory usage
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    callbacks=[learning_rate_reduction, checkpoint_callback],
    workers=2,  
    use_multiprocessing=False
)

# Save the final model in SavedModel format for optimized loading
model.save('new_model_saved')