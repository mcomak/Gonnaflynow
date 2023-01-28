# how to accept cookie consent with selenium python

# libraries & modules & configs
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
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



def catch_date():
    td_date_element = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr//td[@class="fra-m-flights__td-date"]//time')
    date_element = [dt.text.split(', ')[1] for dt in td_date_element]
    return date_element[0]


# # to read the text from all td elements
td_elements = driver.find_elements(By.XPATH, '//table[@class="fra-e-table"]//tbody[@class="fra-e-table__body"]//tr[@class="fra-m-flights__row"]//td')

td_list = [td.text for td in td_elements]
td_list = [j for i, j in enumerate(td_list) if i % 8 not in [0,7]]

for i, value in enumerate(td_list):
    # catching dates and place in Date column
    df.loc[i//6 , "Date"] = catch_date()

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

