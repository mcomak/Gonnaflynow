

from selenium import webdriver

PATH = "/Users/Mertcan/Documents/DataOps/DEng/web_scratching/chromedriver"


driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)

driver.get("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")

# Xpath you just copied
news_path = '/html/body/c-wiz/div/div[2]/main/div[2]/c-wiz/section/div[2]/div/div[2]/c-wiz/c-wiz/article/div[1]/div[2]/div/h4'

# to get that element
link = driver.find_element_by_xpath(news_path).click()

# to read the text from that element
print(link.text)

print(driver.title)
driver.quit()
