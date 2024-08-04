#This file will include a class with instance methods.
#That will be responsible to interact with our website
#After we have some results, to apply filtrations.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        # Update the selector for the star filtration box
        star_filtration_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-filters-group="class"]'))
        )
        
        for star_value in star_values:
            try:
                star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
                star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, 'div[data-filters-item]')
                
                for star_element in star_child_elements:
                    if f'{star_value} stars' in star_element.get_attribute('innerHTML'):
                        star_element.click()
                        break
            except StaleElementReferenceException:
                print(f"StaleElementReferenceException encountered for {star_value} stars. Retrying...")
                star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
                star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, 'div[data-filters-item]')
                for star_element in star_child_elements:
                    if f'{star_value} stars' in star_element.get_attribute('innerHTML'):
                        star_element.click()
                        break