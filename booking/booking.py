import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += os.pathsep + self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        # Adding a wait to ensure the currency options are loaded
        WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//button[@data-testid="selection-item"]//div[contains(text(), "{currency}")]'))
        )

        selected_currency_element = self.find_element(By.XPATH, f'//button[@data-testid="selection-item"]//div[contains(text(), "{currency}")]')
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.CSS_SELECTOR, 'input[name="ss"]')
        search_field.clear()
        search_field.send_keys(place_to_go)

        # Adding a wait to ensure the autocomplete results are loaded
        WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, 'autocomplete-result-0'))
        )

        first_result = self.find_element(By.ID, 'autocomplete-result-0')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'))
        )
        check_in_element.click()

        check_out_element = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'))
        )
        check_out_element.click()

    def select_adults(self, count=1):
        # Open the occupancy selection
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        # Decrease adults to 1
        while True:
            decrease_adults_element = self.find_element(By.CSS_SELECTOR, 'button.dba1b3bddf.e99c25fd33[aria-hidden="true"]')
            decrease_adults_element.click()
            # If the value of adults reaches 1, then we should get out of the while loop
            adults_value_element = self.find_element(By.CSS_SELECTOR, 'span.fb7047f72a[aria-hidden="true"]')
            adults_value = adults_value_element.text  # Should give back the adults count

            if int(adults_value) == 1:
                break

        # Increase the adults count to the desired number
        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button.dba1b3bddf.e99c25fd33.d1821e6945[aria-hidden="true"]')

        for _ in range(count - 1):
            increase_button_element.click()
   
    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
    
    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)

        #filtration.sort_price_lowest_first()
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)