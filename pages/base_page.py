from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            accept_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='wt-cli-accept-all-btn']")
                )
            )
            accept_button.click()
        except TimeoutException:
            pass

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def type(self, locator, text: str):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )
        return element
