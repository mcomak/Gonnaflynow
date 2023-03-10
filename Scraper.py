from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
import numpy as np

pd.options.display.max_columns = None
pd.options.display.width = None


class Scraper:
    # Global class variable to store the driver instance
    driver = None

    @staticmethod
    def init_driver():
        if not Scraper.driver:
            Scraper.driver = webdriver.Chrome(ChromeDriverManager().install())
            Scraper.driver.set_window_size(1920, 1080)

    def __init__(self,location='frankfurt'):
        Scraper.init_driver()
        self.driver = Scraper.driver
        self.th_list = []
        self.td_list = []
        self.img_alt_list = []
        self.date_obj = ''
        self.df = pd.DataFrame()
        self.location = location

    def open_tab(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)

    def open_url(self):
        if self.location == 'istanbul':
            self.open_tab('https://www.istairport.com/en/passenger/flight/departure?locale=en')
            button_loc = ""
            # No cookie acception for istanbul url
        if self.location == 'frankfurt':
            self.open_tab('https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html')
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
                          'Flight', 'Status', 'Codeshare', 'Terminal','Halle','Gate','Checkin',
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
        self.date_obj = self.date_obj.strftime('%d.%m.%Y')
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
                    try:
                        # try if value can be splited. If not pass it.
                        self.df.loc[i // 9, "Terminal"] = value.split(",")[0]
                        self.df.loc[i // 9, "Halle"] = value.split(",")[1]
                        self.df.loc[i // 9, "Gate"] = value.split(",")[2]
                        self.df.loc[i // 9, "Checkin"] = value.split(",")[3]
                    except:
                        pass
                elif (i % 9) == 8:
                    self.df.loc[i // 9, "Click"] = value
            self.df = self.df.drop(columns=['Click'],axis=1)
        self.delay_calc()
        # Date datatype converting
        self.date_convertor()
        return self.df

    def quit_driver(self):
        self.driver.quit()


    # Raw Data Manipulation

    def date_convertor(self):

        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y')
        return self.df

    def add_day(self,value):
        if value < pd.Timedelta(days=0):
            return value + pd.Timedelta(days=1)
        else:
            return value

# delay column creating:
#     def delay_calc(self, col3="Estimated_timedelta", col4="Planned_timedelta"):
#         # Timedelta columns has created by Planned and Estimated columns
#         self.df[col3] = pd.to_datetime(self.df['Planned'], format='%H:%M')
#         self.df[col4] = pd.to_datetime(self.df["Estimated"], format='%H:%M')
#         # Substracting for Delay time
#         self.df['Delay'] = (self.df[col3] - self.df[col4])
#         # Delay time is converting to int as minute from minus
#         self.df['Delay'] = self.df['Delay'].dt.total_seconds().astype(int) / 60
#         # If Estimated is earlier than planned, Delay will be negative
#         self.df.loc[self.df['Delay'] < 0, 'Delay'] = self.df.loc[self.df['Delay'] < 0, 'Delay'] * -1
#         # Dropping supporting timedelta columns
#         self.df = self.df.drop(columns=[col3, col4])
#         return self.df

    def delay_calc(self, col3="Estimated_timedelta", col4="Planned_timedelta"):
        # Timedelta columns has created by Planned and Estimated columns
        self.df[col3] = pd.to_datetime(self.df['Planned'], format='%H:%M')
        self.df[col4] = pd.to_datetime(self.df["Estimated"], format='%H:%M')
        # Substracting for Delay time

        # If Estimated is earlier than Planned, it should be on next day of planned time
        self.df[col4] = np.where(self.df[col4] < self.df[col3], self.df[col3] + pd.Timedelta(days=1),
                                   self.df[col3])
        self.df['Delay'] = ((self.df[col3] - self.df[col4]).dt.total_seconds().astype(int)) / 60

        # Dropping supporting timedelta columns
        self.df = self.df.drop(columns=[col3, col4])
        return self.df


# sc = Scraper(location='frankfurt')
# sc = Scraper(location='istanbul')
# sc.inject_to_df()
# sc.df
# sc.quit_driver()
# print(sc.df)