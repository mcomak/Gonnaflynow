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
df.columns = ['Date', 'Airline', 'Departure', 'Estimation', 'Destination, via',
       'Flight', 'State', 'Codeshare', 'Terminal, Halle, Gate, Check-in',
       'Click']

# # Find empty column names
# empty_cols = [col for col in df.columns if col.strip() == '']
#
# # Drop empty column names
# df.drop(empty_cols, axis=1, inplace=True)

def check_date(date_string):
    try:
        datetime.strptime(date_string, '%A, %d %B %Y')
        return True
    except ValueError:
        return False

def convert_date(date_string):
    date_obj = datetime.strptime(date_string, '%A, %d %B %Y')
    date_obj = date_obj.strftime('%d-%m-%Y')
    return date_obj

# td elements with dates
td_list = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr//td')
td_list = [td.text for td in td_list]

# Capturing from Image:
img_elements = driver.find_elements(By.XPATH, "//td[@class='fra-m-flights__td-airline']/img")
img_alt_list = [img_element.get_attribute('alt') for img_element in img_elements]

# insert dates in td_list
for i,j in enumerate(td_list):
    if (i % 9) == 0:
        if check_date(j) == False:
           td_list.insert(i, td_list[( i // 9 - 1 ) * 9])

for i,j in enumerate(td_list):
    if i % 9 == 0:
        td_list[i] = convert_date(j)

# Distribute other table-values to columns
for i,value in enumerate(td_list):
    if (i % 9) == 0:
        df.loc[i // 9, "Date"] = value
    elif (i % 9) == 1:
        df.loc[i // 9, "Airline"] = str(df.loc[i//9,"Flight"]).split(' ')[0]
    elif (i % 9) == 2:
        if len(value.split()) > 1:
            val_list = value.split('\n')
            df.loc[i // 9, "Departure"] = val_list[0]
            df.loc[i // 9, "Estimation"] = val_list[1]
        else:
            df.loc[i // 9, "Departure"] = value
            df.loc[i // 9, "Estimation"] = value
    elif (i % 9) == 3:
        df.loc[i//9, "Destination, via"] = value
    elif (i % 9) == 4:
        df.loc[i//9, "Flight"] = value
    elif (i % 9) == 5:
        df.loc[i//9, "State"] = value
    elif (i % 9) == 6:
        df.loc[i//9, "Codeshare"] = value
    elif (i % 9) == 7:
        df.loc[i//9, "Terminal, Halle, Gate, Check-in"] = value
    elif (i % 9) == 8:
        df.loc[i//9, "Click"] = value


str(df.loc[i//9,"Flight"]).split(' ')[0]

print(df)


# Data Manipulation




driver.quit()

