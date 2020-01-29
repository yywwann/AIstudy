from bs4 import BeautifulSoup
from urllib.request import urlopen

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/basic-structure.html").read().decode('utf-8')
# print(html)

soup = BeautifulSoup(html, features='html.parser')
print(soup.h1)
print('\n', soup.p)
all_href = soup.find_all('a')
print('\n', all_href)
all_href = [l['href'] for l in all_href]
print('\n', all_href)