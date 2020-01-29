from urllib.request import urlopen
import re

# if has Chinese, apply decode()
html = urlopen(
    "https://morvanzhou.github.io/static/scraping/basic-structure.html"
).read().decode('utf-8')
res = re.findall(r"<title>(.+?)</title>", html)
print("\nPage title is: ", res[0])
