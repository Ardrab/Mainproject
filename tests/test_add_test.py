from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException

# Initialize WebDriver using the Service object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def accept_alert_if_present():
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()  # or alert.dismiss() if you want to cancel
    except TimeoutException:
        pass  # No alert present, proceed as normal

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")  # Replace with your login URL
    
    # Debugging: Print the page source
    print(driver.page_source)

    # Step 2: Locate the email field and input the credentials
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

    # Step 4: Wait for redirection to labindex page after login
    WebDriverWait(driver, 20).until(
        EC.url_contains("labindex")
    )

    # Step 5: Locate the "Add Tests" dropdown and click it
    add_tests_dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "addDropdown"))
    )
    add_tests_dropdown.click()

    # Step 6: Select "Add Test" from the dropdown
    add_test_option = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Add Test"))
    )
    add_test_option.click()

    # Step 7: Wait for the add test page to load
    WebDriverWait(driver, 20).until(
        EC.url_contains("lab/addtestname")
    )

    # Step 8: Locate the test name field and input a test name
    test_name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "test_name"))
    )
    test_name_input.send_keys("123")  # Change this to a valid test name

    # Step 9: Submit the form
    test_name_input.send_keys(Keys.RETURN)

    # Step 10: Check for alerts after form submission
    accept_alert_if_present()

    # Step 11: Wait for redirection to labindex after submitting the form
    WebDriverWait(driver, 20).until(
        EC.url_contains("labindex")
    )

    print("Test added successfully. Redirected to labindex.")

except UnexpectedAlertPresentException as e:
    print("Error: An unexpected alert is present. Details:", e)
    driver.save_screenshot("alert_error.png")
    print("Screenshot saved as alert_error.png")
    accept_alert_if_present()  # Handle the alert if needed

except TimeoutException as e:
    print("Error: Timeout while waiting for an element. Details:", e)
    driver.save_screenshot("timeout_error.png")
    print("Screenshot saved as timeout_error.png")

except NoSuchElementException as e:
    print("Error: Could not find an element. Details:", e)
    driver.save_screenshot("element_error.png")
    print("Screenshot saved as element_error.png")

finally:
    # Step 12: Close the browser after the test
    time.sleep(2)
    driver.quit()
