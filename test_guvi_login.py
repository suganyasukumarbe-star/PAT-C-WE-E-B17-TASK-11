import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestGuviLogin:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Initializes the browser session before each test and
        ensures proper closure after execution.
        """
        # Initialize Chrome driver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        # Step 1: Visit the home URL
        self.driver.get("https://guvi.in")

        yield

        # Step 4: Close the browser and stop automation
        self.driver.quit()

    def test_positive_login_flow(self):
        """
        Positive test case: Validates the migration to the sign-in URL,
        verifies input fields visibility/state, and checks submit button behavior.
        """
        # Step 2: Click the Login button to navigate to the sign-in portal
        # Finding the login button on the landing homepage
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_btn.click()

        # Validation 1: Verify the URL has changed correctly to the sign-in page
        expected_login_url = "https://guvi.insign-in/"
        self.wait.until(EC.url_to_be(expected_login_url))
        assert self.driver.current_url == expected_login_url, "URL validation failed after clicking login!"

        # Validation 2: Ensure Username and Password input fields are visible and enabled
        email_field = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))
        password_field = self.driver.find_element(By.ID, "password")

        assert email_field.is_displayed() and email_field.is_enabled(), "Email input field is not active!"
        assert password_field.is_displayed() and password_field.is_enabled(), "Password input field is not active!"

        # Step 3: Input valid credentials (REMOVED / MASKED FOR PRIVACY)
        email_field.send_keys("cv11821@gmail.com")
        password_field.send_keys("s1994@CSE#1")

        # Validation 3: Ensure the submit login button works properly
        submit_btn = self.driver.find_element(By.ID, "login-btn")
        assert submit_btn.is_displayed() and submit_btn.is_enabled(), "Submit button is not functional!"

        # Perform click to log in
        submit_btn.click()

    def test_negative_login_with_invalid_credentials(self):
        """
        Negative test case: Validates system behavior when bad inputs are delivered.
        """
        # Step 2: Navigate to sign-in page
        login_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        login_btn.click()

        self.wait.until(EC.url_to_be("https://guvi.insign-in/"))

        email_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "password")
        submit_btn = self.driver.find_element(By.ID, "login-btn")

        # Supplying deliberately faulty credentials
        email_field.send_keys("invalid_user_test@guvi.com")
        password_field.send_keys("WrongPassword999")
        submit_btn.click()

        # Verify an error notification banner is prompted to the user
        error_banner = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-message"))
        )
        assert error_banner.is_displayed(), "Negative validation failed: Error message was not shown."
