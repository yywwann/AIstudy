import requests
import webbrowser
param = {"wd": "莫烦Python"}  # 搜索的信息
r = requests.get('http://www.baidu.com/s', params=param)
print(r.url)
webbrowser.open(r.url)