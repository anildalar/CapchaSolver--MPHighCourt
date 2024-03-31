import os
import numpy as np
import cv2
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Step 1: Load and preprocess the images
def load_images(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
            # Resize the image to desired dimensions
            img = cv2.resize(img, (20, 22))  # Adjust dimensions as needed
            # Normalize the image
            img = img / 255.0
            images.append(img)
            # Extract label from last character of filename
            label = int(filename[-5])
            labels.append(label)
    return np.array(images), np.array(labels)

# Step 2: Prepare the data for training
images, labels = load_images('captcha/split')

#print('images >>>',images)
#print('labels >>>',labels)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# Step 3: Design and compile the Sequential model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(20, 22)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Step 4: Train the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# Step 5: Evaluate the model's performance
test_loss, test_acc = model.evaluate(X_val, y_val, verbose=2)
print('\nTest accuracy:', test_acc)

# Define the filename
filename = 'modelo.h5'

# Check if the file exists
if os.path.exists(filename):
    # Remove the existing file
    os.remove(filename)
# Save the model using native Keras format
model.save(filename)