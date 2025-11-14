import time
from pages.home_page import HomePage
from pages.qa_jobs_page import QAJobsPage


def test_home_page_is_opened(driver):
    home = HomePage(driver)
    home.open_home()
    assert home.is_opened(), "Home page could not be opened!"


def test_careers_page_visibility(driver):

    home = HomePage(driver)
    home.open_home()
    time.sleep(2)
    careers_page = home.go_to_careers()
    assert careers_page.is_opened(), "Careers page not opened!"
    assert careers_page.check_locations_block_visible(), "'Our Locations' block not visible!"
    assert careers_page.check_teams_block_visible(), "'See all teams' (Teams) block not visible!"
    assert careers_page.check_life_at_insider_block_visible(), "'Life at Insider' block not visible!"


def test_qa_jobs_after_filters(driver):

    qa_jobs = QAJobsPage(driver)
    qa_jobs.open()
    time.sleep(2)
    qa_jobs.click_see_all_jobs()
    time.sleep(2)
    qa_jobs.filter_by_location_istanbul()
    qa_jobs.filter_by_department_qa()

    cards = qa_jobs.get_job_cards()
    time.sleep(2)
    assert len(cards) > 0, "Job list is empty after applying filters!"


def test_qa_jobs_content(driver):

    qa_jobs = QAJobsPage(driver)
    qa_jobs.open()
    qa_jobs.click_see_all_jobs()
    time.sleep(2)
    qa_jobs.filter_by_location_istanbul()
    time.sleep(1)
    qa_jobs.filter_by_department_qa()
    time.sleep(2)

    qa_jobs.verify_jobs_content(
        expected_dep="Quality Assurance",
        expected_loc="Istanbul, Turkiye",
        expected_pos ="Quality Assurance"
    )

def test_view_role_redirects_to_lever(driver):

    qa_jobs = QAJobsPage(driver)
    qa_jobs.open()
    time.sleep(1)
    qa_jobs.click_see_all_jobs()
    time.sleep(3)
    qa_jobs.filter_by_location_istanbul()
    time.sleep(1)
    qa_jobs.filter_by_department_qa()
    qa_jobs.view_role_and_check_lever()
