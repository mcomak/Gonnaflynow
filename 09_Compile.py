from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime

pd.options.display.max_columns = None
pd.options.display.width = None


class Scraper:
    def __init__(self,url='https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html',\
                 button_loc="button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']",\
                 header_xpath='//table[@class="fra-e-table"]//thead[@class="fra-e-table__header"]//tr//th',location='frankfurt'):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.th_list = []
        self.td_list = []
        self.df = pd.DataFrame()
        self.url = url
        self.button_loc = button_loc
        self.header_xpath = header_xpath
        self.location = location

    def open_url(self):
        self.driver.get(self.url)
        # Accept cookie consent
        try:
            # shadow
            self.shadow = Shadow(self.driver)
            time.sleep(5)
            self.button = self.shadow.find_element(self.button_loc)
            text = self.button.text  # get text of the button
            self.button.click()  # click the button
        except:
            pass
        return self.driver

    def get_table_headers(self):
        self.accept_cookie_consent()
        th_elements = self.driver.find_elements(By.XPATH, self.header_xpath)
        self.th_list = [td.text for td in th_elements]
        return self.th_list

    def create_df(self):
        if self.location == 'istanbul':
            self.df = pd.DataFrame(columns=self.th_list)
        if self.location == 'frankfurt':
            self.df.columns = ['Date', 'Airline', 'Departure', 'Estimation', 'Destination, via',
                               'Flight', 'State', 'Codeshare', 'Terminal, Halle, Gate, Check-in',
                               'Click']
        return self.df

    def get_table_data(self):
        td_elements = self.driver.find_elements(By.XPATH, "//td")
        self.td_list = [td.text for td in td_elements]
        self.td_list = [j for i, j in enumerate(self.td_list) if i % 11 not in [2, 10]]


sc = Scraper()
sc.open_url(url='https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html')
sc.accept_cookie_consent(button_loc="button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']"
                              ,url='https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html')
