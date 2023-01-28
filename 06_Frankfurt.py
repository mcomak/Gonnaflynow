# how to accept cookie consent with selenium python

# libraries & modules & configs
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from datetime import datetime
pd.options.display.max_columns = None
pd.options.display.width = None

# Set the location of our chrome driver
s = Service('/Users/Mertcan/Documents/DataOps/DEng/web_scratching/chromedriver')

# Initialize the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
shadow = Shadow(driver)
driver.get("https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html")

time.sleep(5)
button = shadow.find_element("button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']")
# Interact with the button
text = button.text # get text of the button
button.click() # click the button

# table column names finding
th_elements = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//thead[@class="fra-e-table__header"]//tr//th')
th_list = [th.text for th in th_elements]



df = pd.DataFrame(columns=th_list)
df = df.assign(Date=[])
df.insert(0,"Date",df.pop("Date"))
df = df.assign(Estimation=[])
df.insert(3,"Estimation",df.pop("Estimation"))
# Find empty column names
empty_cols = [col for col in df.columns if col.strip() == '']

# Drop empty column names
df.drop(empty_cols, axis=1, inplace=True)

def catch_date(date_string):
    try:
        datetime.strptime(date_string, '%A, %d %B %Y')
        return True
    except ValueError:
        return False

# td elements with dates
td_with_dates = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr//td')
# td elements w/o dates
td_wo_dates = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr[@class="fra-m-flights__row"]//td')

td_list_with_dates = [td.text for td in td_with_dates]
td_list_wo_dates = [td.text for td in td_wo_dates]
td_list_wo_dates = [j for i, j in enumerate(td_list_wo_dates) if i % 8 not in [0,7]]

for i,j in enumerate(td_list):
    if catch_date(j) == False :
        if



for i, value in enumerate(td_list):
    # catching dates and place in Date column
    if catch_date(value) == True:


    # Distrupute other table-values to columns
    if (i % 6) == 0:
        if len(value.split()) > 1:
            val_list = value.split('\n')
            df.loc[i // 6, "Departure"] = val_list[0]
            df.loc[i // 6, "Estimation"] = val_list[1]
        else:
            df.loc[i // 6, "Departure"] = value
            df.loc[i // 6, "Estimation"] = value
    elif (i % 6) == 1:
        df.loc[i//6, "Destination, via"] = value
    elif (i % 6) == 2:
        df.loc[i//6, "Flight"] = value
    elif (i % 6) == 3:
        df.loc[i//6, "State"] = value
    elif (i % 6) == 4:
        df.loc[i//6, "Codeshare"] = value
    elif (i % 6) == 5:
        df.loc[i//6, "Terminal, Halle, Gate, Check-in"] = value

# adding day to morrow delays
def add_day(value):
    if value < pd.Timedelta(days=0):
        return value + pd.Timedelta(days=1)
    else:
        return value

# delay calculation
def rotar_calc(df,col1,col2,col3 = "Estimation",col4 = "Planned"):
    df[col3] = pd.to_datetime(df[col1], format='%H:%M')
    df[col4] = pd.to_datetime(df[col2], format='%H:%M')
    df['rötar'] = df1[col4] - df[col3]
    df = df.drop(columns=[col3,col4])
    df['rötar'] = df['rötar'].apply(add_day)
    return df

df = rotar_calc(df,'Planlanan','Tahmini')
filtered_df = df.query("Durum == 'Kalktı' | Durum == 'İptal'")


driver.quit()

