import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class WhiskyBaseFormsCheck(unittest.TestCase):
    website = "http://www.python.org"

    def setUp(self):
        self.driver = webdriver.Chrome("E:/Git/Projekt-Programistyczny/testy_selenium/chromedriver.exe")
        self.driver.get(self.website)

    def test_searchProduct(self):
        driver = self.driver

        search_input = driver.find_element(by=By.ID, value="searchProduct")
        search_input.clear()
        search_input.send_keys("Test")
        search_input.send_keys(Keys.RETURN)

        filter_button = driver.find_element(by=By.ID, value="filterButton")
        filter_button.click()

        scrollarea = driver.find_element(by=By.CLASS_NAME, value="scrollarea")
        articles = scrollarea.find_elements(by=By.TAG_NAME, value="article")
        test = True
        if len(articles) == 0:
            test = False
        assert test

    def test_rate_more_less(self):
        driver = self.driver

        rate_input = driver.find_element(by=By.NAME, value="rate")
        rate_input.clear()
        rate_input.send_keys("100")
        rate_input.send_keys(Keys.RETURN)

        rate2_input = driver.find_element(by=By.NAME, value="rate2")
        rate2_input.clear()
        rate2_input.send_keys("50")
        rate2_input.send_keys(Keys.RETURN)

        filter_button = driver.find_element(by=By.ID, value="filterButton")
        filter_button.click()

        scrollarea = driver.find_element(by=By.CLASS_NAME, value="scrollarea")
        articles = scrollarea.find_elements(by=By.TAG_NAME, value="article")
        test = True
        if len(articles) == 0:
            test = False
        assert test


    def test_rate_text(self):
        driver = self.driver

        rate_input = driver.find_element(by=By.NAME, value="rate")
        rate_input.clear()
        rate_input.send_keys("Test")
        rate_input.send_keys(Keys.RETURN)

        filter_button = driver.find_element(by=By.ID, value="filterButton")
        filter_button.click()

        scrollarea = driver.find_element(by=By.CLASS_NAME, value="scrollarea")
        articles = scrollarea.find_elements(by=By.TAG_NAME, value="article")
        test = True
        if len(articles) == 0:
            test = False
        assert test

    def test_rate2_text(self):
        driver = self.driver

        rate2_input = driver.find_element(by=By.NAME, value="rate")
        rate2_input.clear()
        rate2_input.send_keys("Test")
        rate2_input.send_keys(Keys.RETURN)

        filter_button = driver.find_element(by=By.ID, value="filterButton")
        filter_button.click()

        scrollarea = driver.find_element(by=By.CLASS_NAME, value="scrollarea")
        articles = scrollarea.find_elements(by=By.TAG_NAME, value="article")
        test = True
        if len(articles) == 0:
            test = False
        assert test

    def test_sort(self):
        driver = self.driver

        sort_select = Select(driver.find_element(by=By.NAME, value='sort'))
        sort_select.select_by_value('alfabet')

        filter_button = driver.find_element(by=By.ID, value="filterButton")
        filter_button.click()

        scrollarea = driver.find_element(by=By.CLASS_NAME, value="scrollarea")
        articles = scrollarea.find_elements(by=By.TAG_NAME, value="article")
        test = True
        if len(articles) == 0:
            test = False
        assert test

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
