# how to accept cookie consent with selenium python

# libraries & modules & configs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.width = None


# Set the location of our chrome driver & chrome options
s = Service('/Users/Mertcan/Documents/DataOps/DEng/web_scratching/chromedriver')
chromeOptions = Options()
chromeOptions.headless = False

# Url to scrape
driver = webdriver.Chrome(service= s, options=chromeOptions)
driver.get("https://www.istairport.com/en/passenger/flight/departure?locale=en")

# wait 5 sec to open the page before find_elemets
driver.implicitly_wait(5)

# bypass google cookie
try:
    # accept button finding with by methode:
    consent_button = driver.find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and @aria-label='Accept all']")

    # click accept all button for cookies automatically
    consent_button.click()
except:
    pass



# table column names finding
th_elements = driver.find_elements(By.XPATH, "//th[@class= 'border-top-0 text-medium' or @class= 'border-top-0 text-medium not-mobile']")
th_list = [td.text for td in th_elements]

df = pd.DataFrame(columns=th_list)

# # to read the text from all td elements
td_elements = driver.find_elements(By.XPATH, "//td")
# for index, td in enumerate(td_elements):
#     #print(index,td.text)
#     df.loc[index // 11, index % 11] = td.text

td_list = []
[td_list.append(td.text) for td in td_elements]
td_list = [j for i, j in enumerate(td_list) if i % 11 not in [2,10]]


# Iterate through the index of the columns
for i, value in enumerate(td_list):
        if (i % 9) == 0:
            df.loc[i//9, "Date"] = value
        elif (i % 9) == 1:
            df.loc[i//9, "Planned"] = value
        elif (i % 9) == 2:
            df.loc[i//9, "Estimated"] = value
        elif (i % 9) == 3:
            df.loc[i//9, "Airline"] = value
        elif (i % 9) == 4:
            df.loc[i//9, "Flight"] = value
        elif (i % 9) == 5:
            df.loc[i//9, "Departure"] = value
        elif (i % 9) == 6:
            df.loc[i//9, "Arrival"] = value
        elif (i % 9) == 7:
            df.loc[i//9, "Gate"] = value
        elif (i % 9) == 8:
            df.loc[i//9, "Status"] = value

# adding day to morrow delays
def add_day(value):
    if value < pd.Timedelta(days=0):
        return value + pd.Timedelta(days=1)
    else:
        return value

# delay calculation
def rotar_calc(df,col1,col2,col3 = "Estimated_2",col4 = "Planned_2"):
    df[col3] = pd.to_datetime(df[col1], format='%H:%M')
    df[col4] = pd.to_datetime(df[col2], format='%H:%M')
    df['delay'] = df[col4] - df[col3]
    df = df.drop(columns=[col3,col4])
    df['delay'] = df['delay'].apply(add_day)
    return df

df = rotar_calc(df,'Planned','Estimated')
filtered_df = df.query("Status == 'Departed' | Status == 'Canceled'")

print(filtered_df)

driver.quit()

