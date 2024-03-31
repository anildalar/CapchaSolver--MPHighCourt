import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
import requests
import os

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
        self.code_input.returnPressed.connect(self.reload_captcha)  # Connect Enter key press event
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

    def reload_captcha(self):
        # Clear the existing captcha image
         # Retrieve the entered captcha code
        captcha_code = self.code_input.text()
        print("Captcha code:", captcha_code)

        # Clear the input box
        self.code_input.clear()
        if self.captcha_image:
            # Save the captcha image with the input text as filename
            captcha_filename = os.path.join("captcha", f"{captcha_code}.png")
            self.captcha_image.save(captcha_filename)
            # Print message to console log
            print(f"Captcha saved as '{captcha_filename}'.")
            self.captcha_layout.removeWidget(self.captcha_label)
            # Load a new captcha image
            self.captcha_image = self.load_captcha()
            self.display_captcha()
        else:
            print("No captcha image loaded.")

        # Print message to console log
        print("Captcha reloaded.")

    def submit_captcha(self):
        # Retrieve the entered captcha code
        captcha_code = self.code_input.text()
        print("Captcha code:", captcha_code)

        
        # Clear the input box
        self.code_input.clear()

        if self.captcha_image:
            # Save the captcha image with the input text as filename
            captcha_filename = os.path.join("captcha", f"{captcha_code}.png")
            self.captcha_image.save(captcha_filename)
            # Print message to console log
            print(f"Captcha saved as '{captcha_filename}'.")
            self.captcha_layout.removeWidget(self.captcha_label)
            # Load a new captcha image
            self.captcha_image = self.load_captcha()
            self.display_captcha()
        else:
            print("No captcha image loaded.")
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CaptchaWindow()
    window.show()
    sys.exit(app.exec())
