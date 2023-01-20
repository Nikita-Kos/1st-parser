import requests
from bs4 import BeautifulSoup
import json

response = requests.get(url='https://parsinger.ru/html/index1_page_1.html')
res_json = []

cat_links = list(map(lambda c: 'https://parsinger.ru/html/' + c['href'], BeautifulSoup(response.text, 'html.parser').find('div', class_='nav_menu').find_all('a')))

page_links = []
for cat in cat_links:
    response_cat = requests.get(url=cat)
    for link in BeautifulSoup(response_cat.text, 'html.parser').find('div', class_='pagen').find_all('a'):
        page_links.append('https://parsinger.ru/html/' + link['href'])

item_links = []
for page in page_links:
    response_page = requests.get(url=page)
    for item in BeautifulSoup(response_page.text, 'html.parser').find_all('div', 'sale_button'):
        item_links.append('https://parsinger.ru/html/' + item.find('a')['href'])

for i in item_links:
  response = requests.get(url=i)
  response.encoding='utf-8'
  soup = BeautifulSoup(response.text, 'lxml')

  name = soup.find('p', id='p_header').text
  article = soup.find('p', class_='article').text
  desc = soup.find('ul', id='description').find_all('li')
  amount = soup.find('span', id='in_stock').text
  price = soup.find('span', id='price').text
  old = soup.find('span', id='old_price').text

  dict_desc = {}

  for i in desc:
    dict_desc[i['id']] = i.text.split(': ')[1]

  res_json.append({
        'name': name,
        'article': article.split(': ')[1],
        'description': dict_desc,
        'count': amount.split(': ')[1],
        'price': price, 
        'old_price': old,
        'link': url
    })

with open('res.json', 'w', encoding='utf-8') as file:
  json.dump(res_json, file, indent=4, ensure_ascii=False)