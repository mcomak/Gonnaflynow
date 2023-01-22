# How to Bypass the cookies page without stumbling to scratch the web when using Selenium

Cookies are small text files that are stored on your computer or mobile device when you visit a website. They help websites remember your preferences and browsing history, and can be used to personalize your experience. However, when using Selenium for web scraping, cookies can put blocks on your pipeline of web scratching scripts. Websites often use cookies to track user behavior and prevent automated scraping. In order to bypass these blocks and successfully scrape website data, it is important to know how to accept all cookies when using Selenium.

Selenium is a browser automation tool that allows you to interact with web pages in a programmatic way. In order to interact with a web page using Selenium, you need to use a web driver. Chromedriver is a web driver for the Google Chrome browser that allows Selenium to interact with the Chrome browser. Selenium runs Chromedriver as a background process and communicates with it to automate browser actions. By default, Selenium uses Chromedriver but it also supports other web drivers like Firefox, Safari, Edge, and Internet Explorer. In this article, we will focus on how to accept all cookies in Selenium using Chromedriver.

# Requirements

## Step 1 : Install and import Selenium

Before diving into the methods for accepting cookies in Selenium, it’s important to make sure you have the necessary tools and libraries installed. Selenium requires Python to be installed on your computer, you can download it from the official website. Once you have Python installed, you can use pip, the package installer for Python, to install Selenium. You can use the following command to install Selenium using pip:

pip install selenium

After installing selenium in the python environment, these modules and libraries are able to import to python code:

```from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.chrome.service import Service
```

The purpose of the modules and libraries in the given code fragment is as follows:

-   `selenium.webdriver`: This module contains the classes that implement the various browser automation interfaces of Selenium. The  `webdriver.Chrome()`  class is used to interact with the Google Chrome browser.
-   `selenium.webdriver.common.by`: This module provides a set of classes for implementing the various ways of locating elements on a web page. The  `By`  class is used to specify which mechanism to use to locate an element.
-   `selenium.webdriver.chrome.options`: This module provides a way to configure Chrome-specific options when using Selenium. The  `Options()`  class is used to create an instance of ChromeOptions, which can be used to configure various settings like headless mode, disabling extensions, and more.
-   `selenium.webdriver.chrome.service`: This module provides a way to start and stop the ChromeDriver executable. The  `Service()`  class is used to start and stop the ChromeDriver service and configure its properties.
-   `selenium.webdriver.common.keys`: This module provides a set of keys that are used to simulate keyboard events. The  `Keys`  class is used to simulate the pressing of special keys like  `Enter`,  `Tab`,  `Backspace`, and more.

By importing these modules and libraries, we have access to the classes and methods needed to interact with the Chrome browser, configure various settings, and simulate keyboard events.

## Step 2: Download and locate Chromedriver

it’s important to note that in order to use Chromedriver with Selenium, you must have the Google Chrome browser installed on your computer and the version number of Chrome must match the version number of Chromedriver.

You can download Chromedriver from the official website  [here](https://chromedriver.chromium.org/home).

Once you have downloaded the correct version of Chromedriver, you will need to extract the executable file from the archive and add the path to the executable to the system’s environment variable. This will allow Selenium to find and use Chromedriver automatically.

You can check your chrome version by visiting chrome://settings/help on the address bar of chrome browser.

Also, it is important to note that you will need to update Chromedriver periodically as the Chrome browser is updated to ensure compatibility.

By following these steps, you will have the necessary tools and libraries installed and configured to start automating browser actions and scraping website data using Selenium with Chromedriver.

## Step 3: Define Chromedriver file path

If the selenium library has been installed on the python environment and chromedriver has downloaded and extracted to local disk, it is time to code how to bypass the cookie consent page.

# Set the location of our chrome driver  

`s = Service('/Path/chromedriver')`

The first code line after imports is setting up a webdriver for the Chrome browser using Selenium.

Firstly, a  `Service`  object is created with the path to the chrome driver executable. The  `Service`  class is used to control the starting and stopping of the chromedriver server. chromedriver location you extracted has to be written in Service class. For instance:

```
s = Service('C:\chromedriver') for windows  
s = Service('/Users/Mertcan/chromedriver') Unix OS
```

## Step 4: Set options in Chrome browser by Chrome driver

Then, a  `chromeOptions`  the object is created, which is an instance of the  `Options`  class from the  `selenium.webdriver.chrome.options`  module. The  `Options`  the class allows you to set various options for the Chrome browser, such as the headless mode. In this case, the headless property is set to  `False`, which means that the Chrome browser will run with its GUI and be visible on the screen.

Then, the  `webdriver.Chrome()`  the method is called with the  `service`  and  `options`  parameters set to the previously defined  `s`  and  `chromeOptions`  objects respectively. This creates an instance of the Chrome webdriver, which can be used to interact with the Chrome browser and navigate to web pages.

## Step 5: Give URL link to the driver which you want to scratch

Finally, the website URL which you need to scratch is used into  `driver.get()`  method. In this example, I have used a link from google news: “[https://news.google.com/home?hl=en-US&gl=US&ceid=US:en](https://news.google.com/home?hl=en-US&gl=US&ceid=US:en)"

```
chromeOptions = Options()  
chromeOptions.headless = False  
driver = webdriver.Chrome(service= s, options=chromeOptions)  
driver.get("https://news.google.com/home?hl=en-US&gl=US&ceid=US:en")
```
**Output:**

![](https://miro.medium.com/max/1400/1*4Fb9PHCBv5DIZaFDcmfY9Q.png)

The cookies confirmation page got by Chromedriver

## Step 6: How to bypass the cookie page

Normally, the Driver will enter the link, then it will start the process as we plan. But what’s that? There’s an intruder in there. Google is asking our driver, do you want to accept cookies? If this is not accounted for, things could get messy and the code blog will not work. Our goal is to bypass this cookie consent page and then reach the home page, which is our scratching target. Here we go!

In order to manage that, we will accept all cookies automatically with only 2 code rows in python. Firstly, we should dig for some info about  **Accept all**  button in the HTML. For this, Right-click the Accept all button like the following image, then select inspect from the opened menu.

![](https://miro.medium.com/max/1400/1*_DT5Frh9Pq77WuLT3zndXg.png)

Then in the HTML block, press “CTRL + F” to search and write “Accept all”. You can find the “button” element in founds. From this code block, we can take class parts as ‘VfPpkd-LgbsSe’ and  [@aria](http://twitter.com/aria)-label=’Accept all’ in order to indicate the location of the Accept-all button to python.

![](https://miro.medium.com/max/1400/1*74AZYqbYhd3OyA9By-G_Cg.png)

In our code block, we can define it with  `find_element()`  the method of the webdriver object to find it on the page with a specific set of attributes.

The  `By`  attribute is  `By.XPATH`  and the locator string is "//button[contains(@class, 'VfPpkd-LgbsSe') and @aria-label='Accept all']". This means that the  `find_element()`  method will search the page for a button element that has a class attribute that contains the value "VfPpkd-LgbsSe" and an aria-label attribute that has the value "Accept all".

The  `find_element()`  the method returns the first element that matches the specified attributes, so in this case, it will return the first button element on the page that matches the specified attributes. This returned element is assigned to the variable  `consent_button`.

The next step is to click on the “Accept all” button that we located in the previous step. This will automatically accept all the cookies and we will be able to proceed with our web scraping without any interruption. The click() method is a built-in method provided by selenium to interact with elements on a web page, in this case, it is used to simulate a mouse click on the “Accept all” button.

```
try: 
    # accept button finding with by methode:  
    consent_button = driver.find_element(By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and @aria-label='Accept all']")  
  
    # click accept all button for cookies automatically  
    consent_button.click()  
except:  
    pass
```


if an exception is raised when trying to find the "Accept all" button or when trying to click it, the code in the  `except`  block will be executed (which in this case is just  `pass`, so the code will continue to run without stopping). This way, the script will not be interrupted even if the "Accept all" button is not found on the page.

If the code block works smoothly until here, the cookies will be automatically accepted on the cookie page and access to the web scratching page will be provided. Afterwards, it can be checked whether the desired element is captured with a simple Xpath capture operation as follows:

```
#Example Xpath from google news HTML  
news_path = '/html/body/c-wiz/div/div[2]/main/div[2]/c-wiz/section/div[2]/div/div[2]/c-wiz/c-wiz/div/article/h4'  ```
  
```# to get that element  
link = driver.find_element(By.XPATH, news_path)  
```
  
```
# to read the text from that element  
print(link.text)
```

In my example, first new header is stracthed from new page by bypassed cookies as you can see below:
![](https://miro.medium.com/max/1400/1*6-tk3RDqka-unQIYd0aSFQ.png)

Captured data: "Monterey Park shooting: 10 dead in incident after Lunar New Year festival"

Output in Python Console:
![](https://miro.medium.com/max/1400/1*ruRTe3EmyGtaCVUCkSWImQ.png)