from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Step 1: Navigate to the login page
    driver.get('http://localhost:8000/login/')  # Change this URL to your login page URL

    # Step 2: Wait for the email and password input fields to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))

    # Step 3: Find the email and password input fields
    email_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')

    # Step 4: Input the email and password
    email_input.send_keys('admin@gmail.com')
    password_input.send_keys('Admin')

    # Step 5: Submit the form
    password_input.send_keys(Keys.RETURN)

    # Step 6: Wait for the dashboard to load and check title
    WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))

    # Step 7: Check if login was successful by looking for a specific element on the dashboard
    if "Dashboard" in driver.title:
        print("Login successful!")

        # Step 8: Now test the registration form
        # Navigate to the registration form page
        driver.get('http://localhost:8000/admins/addlab/')  # Change this URL to your registration form URL

        # Step 9: Wait for the registration form elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'first_name')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))

        # Step 10: Fill in the registration form
        lab_name_input = driver.find_element(By.NAME, 'first_name')
        email_input = driver.find_element(By.NAME, 'email')

        lab_name_input.send_keys('Zlab')
        email_input.send_keys('zlab@gmail.com')

        # Step 11: Submit the registration form
        registration_form = driver.find_element(By.ID, 'registrationForm')
        registration_form.submit()

        # Step 12: Wait for the response after submission
        # Replace the title check with a URL check
        WebDriverWait(driver, 10).until(EC.url_contains("http://localhost:8000/admins/adminindex/"))  # Adjust the URL as needed

        # Step 13: Check if the registration was successful
        if "Lab" in driver.page_source:  # Adjust the condition based on your success message
            print("Registration successful! Redirected to Admin Index.")
        else:
            print("Registration failed!")

    else:
        print("Login failed!")

finally:
    # Close the driver
    driver.quit()


