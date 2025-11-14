import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage


class QAJobsPage(BasePage):

    qa_url = "https://useinsider.com/careers/quality-assurance/"
    accept_cookies = (By.XPATH, "//*[@id='wt-cli-accept-all-btn']")
    see_all_qa_jobs_button = (By.XPATH, "//a[contains(@class, 'btn') and contains(., 'See all QA jobs')]")
    location_filter_box = (By.XPATH, "//*[@id='top-filter-form']/div[1]/span/span[1]/span/span[2]")
    locations_list = (By.ID,"select2-filter-by-location-results")
    location_option_istanbul = (By.XPATH, "//li[contains(@id,'select2-filter-by-location-result') "
        "and contains(normalize-space(), 'Istanbul, Turkiye')]")
    department_filter_box = (By.XPATH,"//span[@id='select2-filter-by-department-container']")
    department_option_qa = (By.XPATH,"//li[contains(@id,'select2-filter-by-department-result') "
        "and normalize-space()='Quality Assurance']")
    job_list_items = (By.CSS_SELECTOR, "#jobs-list div.position-list-item")
    job_position = (By.CSS_SELECTOR, "p.position-title.font-weight-bold")
    job_department = (By.CSS_SELECTOR, "span.position-department")
    job_location = (By.CSS_SELECTOR, "div.position-location")
    view_role_button = (By.XPATH, "//*[@id='jobs-list']/div/div/a")
    apply_button = (By.XPATH,"//a[contains(text(), 'Apply for this job')]")

    def open(self):
        super().open(self.qa_url)

    def click_see_all_jobs(self):
        self.click(self.see_all_qa_jobs_button)

    def filter_by_location_istanbul(self):
        time.sleep(4)
        self.click(self.location_filter_box)
        container = self.wait.until(
            EC.visibility_of_element_located(self.locations_list)
        )
        time.sleep(1)
        for _ in range(20):
            try:
                istanbul = self.driver.find_element(*self.location_option_istanbul)
                if istanbul.is_displayed():
                    istanbul.click()
                    time.sleep(1)
                    return
            except NoSuchElementException:
                pass
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + 120;",
                container
            )
            time.sleep(0.3)

    def filter_by_department_qa(self):
        self.click(self.department_filter_box)
        time.sleep(1)
        self.click(self.department_option_qa)

    def get_job_cards(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.job_list_items))

    def verify_jobs_content(
        self,
        expected_dep: str = "Quality Assurance",
        expected_loc: str = "Istanbul, Turkiye",
        expected_pos: str = "Quality Assurance"):

        self.scroll_to(self.job_list_items)

        cards = self.get_job_cards()
        assert len(cards) > 0, "Job list is empty after filters!"

        for card in cards:
            department = card.find_element(*self.job_department).text
            location = card.find_element(*self.job_location).text
            position = card.find_element(*self.job_position).text


            assert expected_dep in department, \
                f"Department mismatch. Got: '{department}'"

            assert expected_loc in location, \
                f"Location mismatch. Got: '{location}'"

            assert expected_pos in position, \
                f"Position mismatch. Got: '{position}'"


    def view_role_and_check_lever(self):
        self.get_job_cards()

        button = self.wait.until(
            EC.presence_of_element_located(self.view_role_button)
        )
        time.sleep(2)
        self.scroll_to(self.job_list_items)

        ActionChains(self.driver).move_to_element(button).perform()

        self.wait.until(
            EC.element_to_be_clickable(self.view_role_button)
        ).click()

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        current_url = self.driver.current_url.lower()
        assert "lever.co" in current_url, \
            f"Not redirected to Lever application form. Current URL: {current_url}"

        apply_button = self.wait.until(
            EC.visibility_of_element_located(self.apply_button)
        )
        assert "apply" in apply_button.text.lower(), \
            f"'Apply for this job' button not found. Got text: '{apply_button.text}'"

