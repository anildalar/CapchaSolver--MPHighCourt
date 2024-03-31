from selenium import webdriver

# Initialize Chrome webdriver
driver = webdriver.Chrome()

# Open the webpage containing the captcha
driver.get("https://mphc.gov.in/captcha_new/captcha.php?cache=73554921711854381203")

# Find the captcha image element
captcha_image = driver.find_element_by_id("cp")

# Get the screenshot of the captcha image
captcha_image.screenshot("captcha_screenshot.png")

# Close the webdriver
driver.quit()
