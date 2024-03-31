import cv2
import os
import numpy as np
from tensorflow import keras
import tensorflow as tf


def split(image, captcha_code):
    # Read the modified grayscale image
    gray_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    # Apply additional preprocessing (e.g., Gaussian blur)
    gray_blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply adaptive thresholding
    binary_image = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create the output directory if it doesn't exist
    output_dir = os.path.join("test", "split")
    os.makedirs(output_dir, exist_ok=True)

    # Save each box as a separate image
    # Convert contours to a list before reversing
    contours = list(contours)
    contours.reverse()
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 10:  # Adjust threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if 0.1 < aspect_ratio < 2:  # Adjust aspect ratio range as needed
                box_image = gray_image[y - 5:y + h + 5, x - 5:x + w + 5]  # Extract box region
                # Ensure captcha_code has enough characters before accessing
                print('Captcha Code >>',captcha_code)
                # Reverse the captcha_code
                captcha_code_reversed = captcha_code[::-1]
                if i < len(captcha_code):
                    filename = f"{captcha_code}_{i + 1}_{captcha_code[i]}.png"
                    cv2.imwrite(os.path.join(output_dir, filename), box_image)  # Save box image
                else:
                    print(f"Index {i} out of range for captcha code {captcha_code}. Skipping.")

    print(f'{len(contours)} box images saved in {output_dir}.')

def predict(model, test_image_path):
    # Load the test image
    test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)

    # Split the test image into individual digits
    split(test_image_path, 'test')  # Assuming 'test' is the captcha code for the test image

    # Get paths of individual digit images
    digit_image_paths = [os.path.join("test", "split", filename) for filename in os.listdir(os.path.join("test", "split"))]

    # Load and preprocess individual digit images
    digit_images = []
    for digit_image_path in digit_image_paths:
        digit_img = cv2.imread(digit_image_path, cv2.IMREAD_GRAYSCALE)
        digit_img = cv2.resize(digit_img, (20, 22))  # Resize to match model input shape
        digit_img = digit_img / 255.0  # Normalize
        digit_images.append(digit_img)

    # Predict letters for each digit
    predicted_code = ''
    for digit_img in digit_images:
        digit_img = np.expand_dims(digit_img, axis=0)  # Add batch dimension
        prediction = model.predict(digit_img)
        predicted_label = np.argmax(prediction)
        predicted_code += str(predicted_label)

    return predicted_code

# Load the trained model
loaded_model = keras.models.load_model('modelo.h5')

# Path to the test image
test_image_path = 'test.png'

# Predict the code
predicted_code = predict(loaded_model, test_image_path)

# Display the predicted code
print("Predicted code:", predicted_code)

 