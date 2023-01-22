import requests
from bs4 import BeautifulSoup

# get the data
data = requests.get('https://www.istairport.com/tr/yolcu/ucus-bilgileri/giden-ucuslar')


# load data into bs4
soup = BeautifulSoup(data.text,'html.parser')

flight = soup.find('table', {'id': 'flightstable'})
tbody = flight.find('tbody')

print(flight)