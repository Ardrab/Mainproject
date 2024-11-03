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
        alert.accept()  # Accept the alert
    except TimeoutException:
        pass  # No alert present, proceed as normal

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")  # Replace with your login URL

    # Debugging: Print the page source
    print(driver.page_source)

    # Step 2: Locate the email and password fields and input the credentials
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    # Step 3: Enter login details and submit the form
    email_input.send_keys("krishnaajay2025@mca.ajce.in")  # Enter your email
    password_input.send_keys("Krishna@123")  # Enter your password
    password_input.send_keys(Keys.RETURN)  # Submit the form

    # Step 4: Wait for redirection to labindex page after login
    WebDriverWait(driver, 20).until(
        EC.url_contains("labindex")
    )

    # Step 5: Locate the "Add Tests" dropdown and click it
    add_tests_dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "addDropdown"))
    )
    add_tests_dropdown.click()

    # Step 6: Select "Add Test Types" from the dropdown
    add_test_types_option = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Add Test Types"))
    )
    add_test_types_option.click()

    # Step 7: Wait for the add test types page to load
    WebDriverWait(driver, 20).until(
        EC.url_contains("lab/addtesttypes")  # Adjust based on your URL
    )

    # Step 8: Fill out the Test Name dropdown
    test_name_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'test_id'))
    )
    test_name_dropdown.click()
    test_name_dropdown.send_keys('Complete blood count')  # Replace with the actual test name
    test_name_dropdown.send_keys(Keys.RETURN)

    # Step 9: Fill out the Test Type Names input
    test_type_names_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'tests_names'))
    )
    test_type_names_input.send_keys('Wbc')

    # Step 10: Fill out the Normal Range input
    normal_range_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'normal_range'))
    )
    normal_range_input.send_keys('110-112 mg/dL')

    # Step 11: Fill out the Amount input
    amount_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'amount'))
    )
    amount_input.send_keys('100.00')

    # Step 12: Submit the form
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()
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
    # Step 13: Close the browser after the test
    time.sleep(2)  # Optional wait before closing
    driver.quit()
