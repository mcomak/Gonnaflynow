from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
shadow = Shadow(driver)
driver.get("https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html")
# Find the button element using the data-testid and class attributes
element = shadow.find_element("button[data-testid='uc-accept-all-button'][class='sc-eDvSVe dmPTtj']")

# Interact with the button
text = element.text # get text of the button
element.click() # click the button