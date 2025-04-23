from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def accept_alert_if_present():
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()
    except TimeoutException:
        pass

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")

    # Step 2: Login
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys("krishnaajay2025@mca.ajce.in")
    password_input.send_keys("Krishna@123", Keys.RETURN)

    # Step 3: Wait for labindex page to load
    WebDriverWait(driver, 20).until(EC.url_contains("labindex"))

    # Step 4: Click dropdown toggle
    dropdown_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "addDropdown"))
    )
    dropdown_toggle.click()

    # Step 5: Click "Add Test" from dropdown
    add_test_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add Test"))
    )
    add_test_item.click()

    # Step 6: Wait for "Add Test" page to load
    WebDriverWait(driver, 10).until(EC.url_contains("addtest"))
    print("✅ Navigated to 'Add Test' page.")

    # Step 7: Fill in the test name
    test_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "test_name"))
    )
    test_name_input.send_keys("Vitamin D Test")  # 👉 Change test name as needed

    # Step 8: Click the Save button
    save_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
    save_button.click()

    # Optional: Wait for success message or redirection
    time.sleep(2)  # or add another WebDriverWait if there's a confirmation

    print("✅ Test name submitted successfully.")

except Exception as e:
    print("❌ Failed during test name submission:", e)

finally:
    time.sleep(2)
    driver.quit()
