# how to accept cookie consent with selenium python

# libraries & modules & configs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.width = None


# Set the location of our chrome driver
s = Service('/Users/Mertcan/Documents/DataOps/DEng/web_scratching/chromedriver')
chromeOptions = Options()
chromeOptions.headless = False

driver = webdriver.Chrome(service= s, options=chromeOptions)
driver.get("https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html")

# wait 5 sec to open the page before find_elemets
driver.implicitly_wait(5)


# Google-cookies bypass
try:
    # accept button finding with by methode:
    consent_button = driver.find_element(By.XPATH, "//button[contains(@class, 'sc-eDvSVe dmPTtj') and 'Accept all']")

    # click accept all button for cookies automatically
    consent_button.click()
except:
    pass

# table column names finding
th_elements = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//thead[@class="fra-e-table__header"]//tr//th')
th_list = [th.text for th in th_elements]


df = pd.DataFrame(columns=th_list)
df.columns
df = df.assign(Date=[])
df.insert(0,"Date",df.pop("Date"))
df = df.assign(Estimation=[])
df.insert(3,"Estimation",df.pop("Estimation"))


def catch_date():
    td_date_element = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr//td[@class="fra-m-flights__td-date"]//time')
    date_element = [dt.text.split(', ')[1] for dt in td_date_element]
    return date_element[0]


# # to read the text from all td elements
td_elements = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr[@class="fra-m-flights__row"]//td')

td_list = [td.text for td in td_elements]

for i, value in enumerate(td_list):
    # catching dates and place in Date column
    df.loc[i//9 , "Date"] = catch_date()

    # Distruputing other table-values to columns
    if (i % 9) == 1:
        if len(value.split()) > 1:
            val_list = value.split('\n')
            df.loc[i//9, "Departure"] = value[0]
            df.loc[i // 9, "Estimation"] = value[1]
        else:
            df.loc[i // 9, "Departure"] = value
    elif (i % 9) == 2:
        df.loc[i//9, "Destination, via"] = value
    elif (i % 9) == 3:
        df.loc[i//9, "Flight"] = value
    elif (i % 9) == 4:
        df.loc[i//9, "State"] = value
    elif (i % 9) == 5:
        df.loc[i//9, "Codeshare	"] = value
    elif (i % 9) == 6:
        df.loc[i//9, "Terminal, Halle, Gate, Check-in"] = value
    elif (i % 9) == 7:
        df.loc[i//9, ""] = value



driver.quit()

# td_list = [j for i, j in enumerate(td_list) if i % 11 not in [2,10]]

# Iterate through the index of the columns




# Timestamp column adding

# df["Tarih"] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y')
# df['Planlanan'] = pd.to_datetime(df['Planlanan'], format='%H:%M')
# df['Tahmini'] = pd.to_datetime(df['Tahmini'], format='%H:%M')
# df['timestamp'] = df.apply(lambda row: row['Tarih'] + row['Planlanan'].time(), axis=1)
# df['timestamp_Planlanan'] = pd.to_datetime(df['Tarih'].dt.strftime('%Y-%m-%d') + ' ' + df['Planlanan'].dt.strftime('%H:%M:%S'), format='%Y-%m-%d %H:%M:%S')
# df['timestamp_Tahmini'] = pd.to_datetime(df['Tarih'].dt.strftime('%Y-%m-%d') + ' ' + df['Tahmini'].dt.strftime('%H:%M:%S'), format='%Y-%m-%d %H:%M:%S')
# df.info()
# filtered_df = df.query("Durum == 'Kalktı' | Durum == 'İptal'")
# df['rotar'] = df['timestamp_Tahmini'] - df['timestamp_Planlanan']
#
# df["Tarih"] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y')


# convert_date (df1,'Planlanan')
# convert_date (df1, 'Tahmini')
# convert_date (df1, 'Tarih', format = '%d.%m.%Y')
#
#
# df['time_difference'] = df['end_time'] - df['start_time']
# df1['rötar'] = df1['Tahmini'] - df1['Planlanan']


# converting date form object dtype
# def convert_date(df, col, format = '%H:%M'):
#
#     if format == '%H:%M':
#         df[col] = pd.to_datetime(df[col], format=format).dt.time
#     else:
#         df[col] = pd.to_datetime(df[col], format=format)
#     return df

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

