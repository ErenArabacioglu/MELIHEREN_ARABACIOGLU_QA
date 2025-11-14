import time
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CareersPage(BasePage):

    locations_section = (By.XPATH,"//h3[normalize-space()='Our Locations']")
    teams_section = (By.XPATH,"//a[normalize-space()='See all teams']")
    life_at_insider_section = (By.XPATH,"//h2[normalize-space()='Life at Insider']")

    def is_opened(self) -> bool:
        return "careers" in self.driver.current_url.lower()

    def check_locations_block_visible(self) -> bool:
        self.scroll_to(self.locations_section)
        time.sleep(1)
        return self.is_visible(self.locations_section)

    def check_teams_block_visible(self) -> bool:
        self.scroll_to(self.teams_section)
        time.sleep(1)
        return self.is_visible(self.teams_section)

    def check_life_at_insider_block_visible(self) -> bool:
        self.scroll_to(self.life_at_insider_section)
        time.sleep(1)
        return self.is_visible(self.life_at_insider_section)
