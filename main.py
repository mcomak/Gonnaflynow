import requests
from bs4 import BeautifulSoup
import time

url = 'https://www.enuygun.com/ucak-bileti/zurih-bologna-guglielmo-marconi-havalimani-zrha-blq/?gidis=17.02.2023&donus=21.02.2023&yetiskin=1&sinif=ekonomi&save=1&geotrip=international&trip=international'
response = requests.get(url)
text = response.text
data = BeautifulSoup(text, 'html.parser')

# since, headings are the first row of the table
headings = data.find_all('span')[0]
headings_list = []  # list to store all headings

for x in headings:
    headings_list.append(x.text)
# since, we require only the first ten columns
headings_list = headings_list[:10]

print('Headings are: ')
for column in headings_list:
    print(column)