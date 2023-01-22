# how to accept cookie consent with selenium python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Set the location of our chrome driver
s = Service('/Users/Mertcan/Documents/DataOps/DEng/web_scratching/chromedriver')

chromeOptions = Options()
chromeOptions.headless = False

driver = webdriver.Chrome(service= s, options=chromeOptions)
# driver.implicitly_wait(10)
driver.get("https://news.google.com/home?hl=en-US&gl=US&ceid=US:en")

try:
    # accept button finding with by methode:
    consent_button = driver.find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and @aria-label='Accept all']")

    # click accept all button for cookies automatically
    consent_button.click()
except:
    pass



# Example Xpath from google news HTML
news_path = '/html/body/c-wiz/div/div[2]/main/div[2]/c-wiz/section/div[2]/div/div[2]/c-wiz/c-wiz/div/article/h4'

# to get that element
link = driver.find_element(By.XPATH, news_path)

# to read the text from that element
print(link.text)