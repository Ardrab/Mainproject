from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize WebDriver using the Service object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")  # Replace with your login URL

    # Step 2: Locate the email and password fields and input the credentials
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    # Step 3: Enter login details and submit the form
    email_input.send_keys("krishnaajay2025@mca.ajce.in")
    password_input.send_keys("Krishna@123")
    password_input.send_keys(Keys.RETURN)

    # Step 4: Sleep for a few seconds to allow redirection after login
    time.sleep(15)  # Adjust the sleep duration based on the page load speed

    # Step 5: Wait for redirection to the labindex page
    WebDriverWait(driver, 30).until(
        EC.url_contains("labindex")
    )

    print("Login successful. Redirected to labindex.")

except TimeoutException as e:
    print("Error: Timeout while waiting for an element. Details:", e)
    driver.save_screenshot("timeout_error.png")
    print("Screenshot saved as timeout_error.png")

except NoSuchElementException as e:
    print("Error: Could not find an element. Details:", e)
    driver.save_screenshot("element_error.png")
    print("Screenshot saved as element_error.png")

finally:
    # Close the browser after the test
    time.sleep(2)
    driver.quit()
