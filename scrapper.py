import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = 'https://www.worldometers.info/coronavirus/#countries'

headers = {
  "User-Agents": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def extract_global(soup):
  counts = [n.text for n in soup.find_all('div', class_= 'maincounter-number')]
  return counts

def stats_global(soup):
  counts = extract_global(soup)
  data = {}
  data['totalCases'] = counts[0]
  data['totalDeaths'] = counts[1]
  data['totalRecovered'] = counts[2]

  print("GLOBAL STATISTICS")
  print()

  print("Total Cases: %s" %data['totalCases'])
  print("Total Deaths: %s" %data['totalDeaths'])
  print("Total Recovered: %s" %data['totalRecovered'])
  print()


def extract_countries(soup):
  countries = []
  table = soup.find('table')
  tableBody = table.find('tbody')

  rows = tableBody.find_all('tr')

  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    countries.append([ele for ele in cols if ele])

  for country in countries[:100]:

    if country[0].isnumeric():
      if len(country) > 5:
        country.pop(0)
        get_country(country[0], country)
    else:
      get_country(country[0], country)
     
       
def get_country(country, data):
  print("__________________")
  print(country)
  print("__________________")
  print()
  print("New Cases: %s" % data[2])
  print("Total Cases: %s" % data[1])
  print("Total Recovered: %s" % data[5])
  print("Total Deaths: %s" % data[3])


def scrapper_data_covid():
  web = requests.get(URL, headers, timeout=5)
  if web.status_code != 200:
      return None
  soup = BeautifulSoup(web.content, "html.parser")

  d = datetime.now().strftime("%m/%d/%Y -- %I:%M %p")

  print("Updated at: %s" %d)

  stats_global(soup)
  extract_countries(soup)


scrapper_data_covid()