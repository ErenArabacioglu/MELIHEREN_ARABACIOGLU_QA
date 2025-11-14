import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class HomePage(BasePage):

    URL = "https://useinsider.com/"

    company_menu = (By.XPATH, "//a[@id='navbarDropdownMenuLink' and normalize-space()='Company']")
    careers_link = (By.XPATH, "//a[contains(@href, '/careers') and normalize-space()='Careers']")

    def open_home(self):
        self.open(self.URL)

    def is_opened(self) -> bool:
        return "Insider" in self.driver.title

    def go_to_careers(self):
        company_el = self.wait.until(EC.visibility_of_element_located(self.company_menu))

        ActionChains(self.driver).move_to_element(company_el).perform()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(self.careers_link)).click()

        from .careers_page import CareersPage
        return CareersPage(self.driver)
