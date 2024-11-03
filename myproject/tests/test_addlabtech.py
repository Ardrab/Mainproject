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
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()  # Accept the alert
        return True
    except TimeoutException:
        return False  # No alert present

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8000/login")  # Replace with your login URL
    time.sleep(3)  # Wait for 3 seconds

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
    time.sleep(3)  # Wait for 3 seconds

    # Step 4: Wait for redirection to labindex page after login
    WebDriverWait(driver, 20).until(
        EC.url_contains("labindex")
    )
    time.sleep(2)  # Wait for 2 seconds

    # Step 5: Select the "Technicians" dropdown and click "Add Technician"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'technicianDropdown')))
    driver.find_element(By.ID, 'technicianDropdown').click()
    time.sleep(3)  # Wait for 3 seconds

    # Step 6: Wait for the "Add Technician" link to be clickable and click it
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Add Technician')))
    driver.find_element(By.LINK_TEXT, 'Add Technician').click()
    time.sleep(3)  # Wait for 3 seconds

    # Step 7: Wait for the registration form elements to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'first_name')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'lname')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
    time.sleep(2)  # Wait for 2 seconds

    # Step 8: Fill in the registration form
    first_name_input = driver.find_element(By.NAME, 'first_name')
    last_name_input = driver.find_element(By.NAME, 'lname')
    email_input = driver.find_element(By.NAME, 'email')

    first_name_input.send_keys('Lina')  # Ensure this field is filled
    last_name_input.send_keys('B')      # Ensure this field is filled
    email_input.send_keys('linab@gmail.com')  # Ensure this field is filled
    time.sleep(2)  # Wait for 2 seconds

    # Step 9: Submit the registration form
    registration_form = driver.find_element(By.ID, 'registrationForm')
    registration_form.submit()
    time.sleep(3)  # Wait for 3 seconds

    # Step 10: Handle unexpected alert if present
    if accept_alert_if_present():
        print("Handled unexpected alert. Please ensure all fields are filled correctly.")
    
    # Step 11: Wait for the response after submission
    WebDriverWait(driver, 10).until(EC.url_contains("http://localhost:8000/lab/labindex/"))  # Adjust the URL as needed
    time.sleep(3)  # Wait for 3 seconds

    # Step 12: Check if the registration was successful
    if "Lab" in driver.page_source:  # Adjust the condition based on your success message
        print("Registration successful! Redirected to Lab Index.")
    else:
        print("Registration failed!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
