import os
import sys
import cv2
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
import requests

class CaptchaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Captcha Solver')
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)

        # Layout for captcha image
        self.captcha_layout = QVBoxLayout()
        main_layout.addLayout(self.captcha_layout)

        # Load the captcha image
        self.captcha_image = self.load_captcha()
        self.display_captcha()

        # Layout for input box and submit button
        self.input_layout = QHBoxLayout()
        main_layout.addLayout(self.input_layout)

        # Input box for entering captcha code
        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText('Enter Captcha')
        self.code_input.returnPressed.connect(self.submit_captcha)  # Connect Enter key press event
        self.input_layout.addWidget(self.code_input)

        # Button for submitting captcha code
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_captcha)
        self.input_layout.addWidget(self.submit_button)

    def load_captcha(self):
        # Fetch the captcha image from the URL
        captcha_url = "https://mphc.gov.in/captcha_new/captcha.php?cache=73554921711854381203"
        response = requests.get(captcha_url)

        if response.status_code == 200:
            # Load the image using QPixmap
            captcha_image = QPixmap()
            captcha_image.loadFromData(response.content)
            return captcha_image
        else:
            print("Failed to fetch the captcha image.")
            return None

    def display_captcha(self):
        # Display the captcha image
        if self.captcha_image:
            self.captcha_label = QLabel(self)
            self.captcha_label.setPixmap(self.captcha_image)
            self.captcha_layout.addWidget(self.captcha_label)
        
    def saveCaptcha(self):
        # Retrieve the entered captcha code
        captcha_code = self.code_input.text()
        print("Captcha code:", captcha_code)

        # Clear the input box
        self.code_input.clear()
        if self.captcha_image:
            # Save the captcha image with the input text as filename
            captcha_filename = os.path.join("captcha", f"{captcha_code}.png")
            self.captcha_image.save(captcha_filename)
            
            self.split(captcha_filename,captcha_code)
            # Print message to console log
            print(f"Captcha saved as '{captcha_filename}'.")
            self.captcha_layout.removeWidget(self.captcha_label)
            # Load a new captcha image
            self.captcha_image = self.load_captcha()
            self.display_captcha()
        else:
            print("No captcha image loaded.")
        pass
    
    def submit_captcha(self):
        self.saveCaptcha()
        
        
    def split(self,image,captcha_code):
        # Read the modified grayscale image
        gray_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

        # Apply additional preprocessing (e.g., Gaussian blur)
        gray_blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Apply adaptive thresholding
        binary_image = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create the output directory if it doesn't exist
        output_dir = os.path.join("captcha", "split")
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
            pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CaptchaWindow()
    window.show()
    sys.exit(app.exec())
