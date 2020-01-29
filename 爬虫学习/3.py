from bs4 import BeautifulSoup
from urllib.request import urlopen

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/list.html").read().decode('utf-8')
print(html)

soup = BeautifulSoup(html, features='html.parser')

# use class to narrow search
month = soup.find_all('li', {"class": "month"})
for m in month:
    print(m.get_text())

