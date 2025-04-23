from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options to allow geolocation
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1  # 1 = Allow, 2 = Block
})

# Initialize WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def accept_alert_if_present():
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()
    except TimeoutException:
        pass  # No alert

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")

    # Step 2: Locate email and password fields
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    # Step 3: Enter credentials and login
    email_input.send_keys("ardrab62@gmail.com")
    password_input.send_keys("Ardra@124")
    password_input.send_keys(Keys.RETURN)

    # Step 4: Wait until redirected to user index
    WebDriverWait(driver, 20).until(
        EC.url_contains("userindex")
    )

    # Step 5: Go to the page with the location form
    driver.get("http://localhost:8000/user/home_collection")

    # Step 6: Click the "Get Current Location" button
    wait = WebDriverWait(driver, 10)
    get_location_btn = wait.until(EC.element_to_be_clickable((By.ID, "get-location-btn")))
    get_location_btn.click()

    # Step 7: Wait for the location field to populate
    location_input = wait.until(lambda d: d.find_element(By.ID, "location"))
    WebDriverWait(driver, 10).until(lambda d: location_input.get_attribute("value") != "")

    # Step 8: Print the detected location
    print("Detected Location:", location_input.get_attribute("value"))

    # ✅ Success message
    print("✅ Test successful!")

    time.sleep(5)

finally:
    driver.quit()
