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
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.th_list = []
        self.td_list = []
        self.df = pd.DataFrame(columns=self.th_list)

    def open_url(self,url):
        self.driver.get(url)

    def accept_cookie_consent(self,button_loc="button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']")
        try:
            self.shadow = Shadow(self.driver)
            time.sleep(5)
            self.button = self.shadow.find_element(button_loc)
            text = self.button.text # get text of the button
            self.button.click() # click the button
        except:
            pass

    def get_table_headers(self,xpath='//table[@class="fra-e-table"]//thead[@class="fra-e-table__header"]//tr//th'):
        th_elements = self.driver.find_elements(By.XPATH,xpath)
        self.th_list = [td.text for td in th_elements]

    def create_fra_df (self):
        self.df = pd.DataFrame(columns=self.th_list)
        self.df = self.df.assign(Date=[])
        self.df.insert(0, "Date", self.df.pop("Date"))
        self.df = self.df.assign(Estimation=[])
        self.df.insert(3, "Estimation", self.df.pop("Estimation"))
        self.df.columns = ['Date', 'Airline', 'Departure', 'Estimation', 'Destination, via',
                      'Flight', 'State', 'Codeshare', 'Terminal, Halle, Gate, Check-in',
                      'Click']

    def get_table_data(self):
        td_elements = self.driver.find_elements(By.XPATH, "//td")
        self.td_list = [td.text for td in td_elements]
        self.td_list = [j for i, j in enumerate(self.td_list) if i % 11 not in [2, 10]]



