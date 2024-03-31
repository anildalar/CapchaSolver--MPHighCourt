import cv2
import os

# Read the modified grayscale image
gray_image = cv2.imread('c.png', cv2.IMREAD_GRAYSCALE)

# Apply additional preprocessing (e.g., Gaussian blur)
gray_blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Apply adaptive thresholding
binary_image = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a directory to store individual box images
output_dir = 'box_images'
os.makedirs(output_dir, exist_ok=True)

# Save each box as a separate image
for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > 10:  # Adjust threshold as needed
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 0.1 < aspect_ratio < 2:  # Adjust aspect ratio range as needed
            box_image = gray_image[y - 5:y + h + 5, x - 5:x + w + 5]  # Extract box region
            cv2.imwrite(os.path.join(output_dir, f'box_{i}.png'), box_image)  # Save box image

print(f'{len(contours)} box images saved in {output_dir}.')
