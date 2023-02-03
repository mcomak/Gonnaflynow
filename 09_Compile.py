from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

pd.options.display.max_columns = None
pd.options.display.width = None


class Scraper:
    def __init__(self,location='frankfurt'):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.set_window_size(1920, 1080)
        self.th_list = []
        self.td_list = []
        self.img_alt_list = []
        self.date_obj = ''
        self.df = pd.DataFrame()
        self.location = location


    def open_url(self):
        if self.location == 'istanbul':
            self.driver.get('https://www.istairport.com/en/passenger/flight/departure?locale=en')
            button_loc = ""
            # Accept cookie consent
        if self.location == 'frankfurt':
            self.driver.get('https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html')
            button_loc = "button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']"
            # Accept cookie consent

        try:
            # shadow
            self.shadow = Shadow(self.driver)
            time.sleep(5)
            self.button = self.shadow.find_element(button_loc)
            text = self.button.text  # get text of the button
            self.button.click()  # click the button
        except:
            pass

        return self.driver

    def get_table_headers(self):
        self.open_url()
        if self.location == 'istanbul':
            th_elements = self.driver.find_elements(By.XPATH, "//th[@class= 'border-top-0 text-medium' or @class= 'border-top-0 text-medium not-mobile']")
            self.th_list = [td.text for td in th_elements]
        # for frankfurt no need.
        return self.th_list


    def create_df(self):
        self.get_table_headers()
        if self.location == 'istanbul':
            self.df = pd.DataFrame(columns=self.th_list)
        if self.location == 'frankfurt':
            column_names = ['Date', 'Airline', 'Planned', 'Estimated', 'Arrival',
                          'Flight', 'Status', 'Codeshare', 'Terminal, Halle, Gate, Check-in',
                          'Click']
            self.df = pd.DataFrame(columns=column_names)
        return self.df

    # Assisting function for frankfurt date column
    def check_date(self,date_string):
        try:
            datetime.strptime(date_string, '%A, %d %B %Y')
            return True
        except ValueError:
            return False

    # Assisting function for frankfurt date column
    def convert_date(self,date_string):
        self.date_obj = datetime.strptime(date_string, '%A, %d %B %Y')
        self.date_obj = self.date_obj.strftime('%d-%m-%Y')
        return self.date_obj


# td_list fills with url table elements
    def get_table_data(self):
        self.create_df()
        if self.location == 'istanbul':
            td_elements = self.driver.find_elements(By.XPATH, "//td")
            [self.td_list.append(td.text) for td in td_elements]
            self.td_list = [td.text for td in td_elements]
            self.td_list = [j for i, j in enumerate(self.td_list) if i % 11 not in [2, 10]]

            # Capturing airline titles from Image:
            img_elements = self.driver.find_elements(By.XPATH,"//td[@class='not-mobile']/div[@class='airline-brand d-inline-block']/img")
            self.img_alt_list = [img_element.get_attribute('alt').split(' ') for img_element in img_elements]

        if self.location == 'frankfurt':
            # td elements with dates
            self.td_list = self.driver.find_elements(By.XPATH,
                                           '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr//td')
            self.td_list = [td.text for td in self.td_list]

            # insert dates in td_list
            for i, j in enumerate(self.td_list):
                if (i % 9) == 0:
                    if not self.check_date(j):
                        self.td_list.insert(i, self.td_list[(i // 9 - 1) * 9])
            for i, j in enumerate(self.td_list):
                if i % 9 == 0:
                    self.td_list[i] = self.convert_date(j)

            # Capturing airline titles from Image:
            img_elements = self.driver.find_elements(By.XPATH, "//td[@class='fra-m-flights__td-airline']/img")
            self.img_alt_list = [img_element.get_attribute('alt') for img_element in img_elements]

        return self.td_list, self.img_alt_list

    # inject td elements to dataframe
    def inject_to_df(self):
        self.get_table_data()
        if self.location == 'istanbul':
            # Iterate through the index of the columns
            for i, value in enumerate(self.td_list):
                if (i % 9) == 0:
                    self.df.loc[i // 9, "Date"] = value
                elif (i % 9) == 1:
                    self.df.loc[i // 9, "Planned"] = value
                elif (i % 9) == 2:
                    self.df.loc[i // 9, "Estimated"] = value
                elif (i % 9) == 3:
                    self.df.loc[i // 9, "Airline"] = self.img_alt_list[i // 9][0]
                elif (i % 9) == 4:
                    self.df.loc[i // 9, "Flight"] = value
                elif (i % 9) == 5:
                    self.df.loc[i // 9, "Departure"] = value
                elif (i % 9) == 6:
                    self.df.loc[i // 9, "Arrival"] = value
                elif (i % 9) == 7:
                    self.df.loc[i // 9, "Gate"] = value
                elif (i % 9) == 8:
                    self.df.loc[i // 9, "Status"] = value

        if self.location == 'frankfurt':
            for i, value in enumerate(self.td_list):
                if (i % 9) == 0:
                    self.df.loc[i // 9, "Date"] = value
                elif (i % 9) == 1:
                    self.df.loc[i // 9, "Airline"] = self.td_list[(i//9)*9+4].split(" ")[0]
                elif (i % 9) == 2:
                    if len(value.split()) > 1:
                        val_list = value.split('\n')
                        self.df.loc[i // 9, "Planned"] = val_list[0]
                        self.df.loc[i // 9, "Estimated"] = val_list[1]
                    else:
                        self.df.loc[i // 9, "Planned"] = value
                        self.df.loc[i // 9, "Estimated"] = value
                elif (i % 9) == 3:
                    self.df.loc[i // 9, "Arrival"] = value
                elif (i % 9) == 4:
                    self.df.loc[i // 9, "Flight"] = value
                elif (i % 9) == 5:
                    self.df.loc[i // 9, "Status"] = value
                elif (i % 9) == 6:
                    self.df.loc[i // 9, "Codeshare"] = value
                elif (i % 9) == 7:
                    self.df.loc[i // 9, "Terminal, Halle, Gate, Check-in"] = value
                elif (i % 9) == 8:
                    self.df.loc[i // 9, "Click"] = value
        return self.df

    def quit_driver(self):
        self.driver.quit()


sc = Scraper(location='frankfurt')
sc.inject_to_df()
# sc.quit_driver()