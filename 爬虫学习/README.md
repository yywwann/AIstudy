
# 爬虫简介
1. 选着要爬的网址 (url)
2. 使用 python 登录上这个网址 (urlopen等)
3. 读取网页信息 (read() 出来)
4. 将读取的信息放入 BeautifulSoup
5. 使用 BeautifulSoup 选取 tag 信息等 (代替正则表达式)

## 用 Python 登录网页
对网页结构和 HTML 有了一些基本认识以后, 我们就能用 Python 来爬取这个网页的一些基本信息. 首先要做的, 是使用 Python 来登录这个网页, 并打印出这个网页 HTML 的 source code. 注意, 因为网页中存在中文, 为了正常显示中文, `read()` 完以后, 我们要对读出来的文字进行转换, `decode()` 成可以正常显示中文的形式.

```python
from urllib.request import urlopen

# if has Chinese, apply decode()
html = urlopen(
    "https://morvanzhou.github.io/static/scraping/basic-structure.html"
).read().decode('utf-8')
print(html)
```

## 匹配网页内容
所以这里我们使用 Python 的正则表达式 `RegEx` 进行匹配文字

如果我们想用代码找到这个网页的 `title`, 我们就能这样写. 选好要使用的 `tag` 名称 `<title>.` 使用正则匹配.

```python
from urllib.request import urlopen
import re

# if has Chinese, apply decode()
html = urlopen(
    "https://morvanzhou.github.io/static/scraping/basic-structure.html"
).read().decode('utf-8')
res = re.findall(r"<title>(.+?)</title>", html)
print("\nPage title is: ", res[0])

```
如果想要找到中间的那个段落 `<p>`, 我们使用下面方法, 因为这个段落在 HTML 中还夹杂着 tab, new line, 所以我们给一个 `flags=re.DOTALL` 来对这些 tab, new line 不敏感.

```python
res = re.findall(r"<p>(.*?)</p>", html, flags=re.DOTALL)    # re.DOTALL if multi line
print("\nPage paragraph is: ", res[0])
```
最后一个练习是找一找所有的链接, 这个比较有用, 有时候你想找到网页里的链接, 然后下载一些内容到电脑里, 就靠这样的途径了.

```python
res = re.findall(r'href="(.*?)"', html)
print("\nAll links: ", res)
```
# BeautifulSoup 解析网页: 基础

## 安装

```shell
# Python 2+
pip install beautifulsoup4

# Python 3+
pip3 install beautifulsoup4
```

## 简单实用方法
这次我们还是爬一爬上次爬的那个基本网页. `BeautifulSoup` 使用起来非常简单, 我们先按常规读取网页.读取这个网页信息, 我们将要加载进 `BeautifulSoup`, 以 `lxml` 的这种形式加载. 除了 `lxml`, 其实还有很多形式的解析器, 不过大家都推荐使用 `lxml` 的形式. 然后 `soup` 里面就有着这个 HTML 的所有信息. 如果你要输出 `<h1>` 标题, 可以就直接 `soup.h1`.
> 报错:bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?

经过测试发现是lxml的问题，使用 pip install lxml 安装，安装完后，在运行还是一样出错, 经百度、知乎的说法是新的库不支持，新版本语法支持改变了
使用 pip install lxml时，自动安装的是最新 4.2.5版本
* 解决方法一:
    卸载新的换老的就可以了
    pip uninstall lxml
    pip install lxml==3.7.0
* 方法二：
    在报错代码中把函数参数中所有的"lxml"改成"html.parser"
    soup = BeautifulSoup(content, "lxml")
    改成 soup = BeautifulSoup(content, "html.parser")

```python
from bs4 import BeautifulSoup
from urllib.request import urlopen
#if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/basic-structure.html").read().decode('utf-8')
# print(html)
soup = BeautifulSoup(html, features='html.parser')
print(soup.h1)
print('\n', soup.p)
```

如果网页中有过个同样的 tag, 比如链接`<a>`, 我们可以使用 `find_all()` 来找到所有的选项. 因为我们真正的 link 不是在 `<a>` 中间 `</a>`, 而是在 `<a href="link">` 里面, 也可以看做是 `<a>` 的一个属性. 我们能用像 Python 字典的形式, 用 `key` 来读取 `l["href"]`.

```python
"""
<a href="https://morvanzhou.github.io/tutorials/scraping">爬虫教程</a>
"""

all_href = soup.find_all('a')
all_href = [l['href'] for l in all_href]
print('\n', all_href)

# ['https://morvanzhou.github.io/', 'https://morvanzhou.github.io/tutorials/scraping']
```

# BeautifulSoup 解析网页: CSS
## 按 Class 匹配
按 Class 匹配很简单. 比如我要找所有 class=month 的信息. 并打印出它们的 tag 内文字.

```python
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


```

# BeautifulSoup 解析网页: 正则表达
## 正则匹配
我们可以用 soup 将这些 `<img>` tag 全部找出来, 但是每一个 img 的链接(src)都可能不同. 或者每一个图片有的可能是 jpg 有的是 png, 如果我们只想挑选 jpg 形式的图片, 我们就可以用这样一个正则 `r'.*?\.jpg'` 来选取. 把正则的 compile 形式放到 BeautifulSoup 的功能中, 就能选到符合要求的图片链接了.

```python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/table.html").read().decode('utf-8')

soup = BeautifulSoup(html, features='html.parser')

img_links = soup.find_all("img", {"src": re.compile('.*?\.jpg')})
for link in img_links:
    print(link['src'])
```
又或者我们发现, 我想选一些课程的链接, 而这些链接都有统一的形式, 就是开头都会有 `https://morvan.`, 那我就将这个定为一个正则的规则, 让 BeautifulSoup 帮我找到符合这个规则的链接.

```python
course_links = soup.find_all('a', {'href': re.compile('https://morvan.*')})
for link in course_links:
    print(link['href'])
```
# 小练习: 爬百度百科
## 制作爬虫
导入一些模块, 设置起始页. 
并将 `/item/...` 的网页都放在 `his` 中, 做一个备案, 记录我们浏览过的网页.
接着我们先不用循环, 对一个网页进行处理, 走一遍流程, 然后加上循环, 让我们的爬虫能在很多网页中爬取. 
下面做的事情, 是为了在屏幕上打印出来我们现在正在哪张网页上, 网页的名字叫什么.

```ptyhon
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random


base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
url = base_url + his[-1]

html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='html.parser')
print(soup.find('h1').get_text(), '    url: ', his[-1])
```
接下来我们开始在这个网页上找所有符合要求的 `/item/` 网址. 使用一个正则表达式过滤掉不想要的网址形式. 这样我们找到的网址都是 `/item/%xx%xx%xx...` 这样的格式了. 之后我们在这些过滤后的网页中随机选一个, 当做下一个要爬的网页. 不过有时候很不幸, 在 `sub_urls` 中并不能找到合适的网页, 我们就往回跳一个网页, 回到之前的网页中再随机抽一个网页做同样的事.

```python
# find valid urls
sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

if len(sub_urls) != 0:
    his.append(random.sample(sub_urls, 1)[0]['href'])
else:
    # no valid sub link found
    his.pop()
print(his)
```

有了这套体系, 我们就能把它放在一个 for loop 中, 让它在各种不同的网页中跳来跳去.

```python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random


base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

for i in range(500):
    url = base_url + his[-1]

    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("^/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()
```

# 多功能的 Requests
## 安装 requests

```pyhton
# python 2+
pip install requests

# python 3+
pip3 install requests
```
## requests get 请求
首先, 我们固定不动的网址部分是 “http://www.baidu.com/s”, ? 后面的东西都是一些参数 (parameters), 所以我们将这些 parameters 用 python 的字典代替, 然后传入 requests.get() 功能. 然后我们还能用 python (webbrowser模块) 打开一个你的默认浏览器, 观看你是否在百度的搜索页面.

```python
import requests
import webbrowser
param = {"wd": "莫烦Python"}  # 搜索的信息
r = requests.get('http://www.baidu.com/s', params=param)
print(r.url)
webbrowser.open(r.url)
```
## requests post 请求
这些数据包括了:

* Request URL (post 要用的 URL)
* Request Method (post)
* Form Data (post 去的信息)

有了这些记录, 我们就能开始写 Python 来模拟这一次提交 post 了. 根据 `'firstname'` 和 `'lastname'`, 也就是上图里面的 Form data, 组织成一个 python 字典. 让后把这个字典传入 `requests.post()`, 注意, 这里的 post 里面的 url, 不是我们填表时的 url (http://pythonscraping.com/pages/files/form.html), 而是要把 Form 信息提交去的那个网页, 也就是上图中查看到的 Request URL (http://pythonscraping.com/files/processing.php).

```python
data = {'firstname': '莫烦', 'lastname': '周'}
r = requests.post('http://pythonscraping.com/files/processing.php', data=data)
print(r.text)
```

## 上传图片
传照片也是 `post` 的一种, 我们得将本地的照片文件传送到服务器. 我们使用这个网页来模拟一次传照片的过程.
![-w778](https://morvanzhou.github.io/static/results/scraping/3-1-10.png)
如果你留意观察 url, 你会发现, 传送完照片以后的 url 有变动. 我们使用同样的步骤再次检查, 发现, “choose file” 按键链接的 `<input> `是一个叫 `uploadFile` 的名字. 我们将这个名字记下, 放入 python 的字典当一个 “key”.
![](https://morvanzhou.github.io/static/results/scraping/3-1-11.png)
接着在字典中, 使用 open 打开一个图片文件, 当做要上传的文件. 把这个字典放入你的 post 里面的 files 参数. 就能上传你的图片了, 网页会返回一个页面, 将你的图片名显示在上面.

```python
file = {'uploadFile': open('./image.png', 'rb')}
r = requests.post('http://pythonscraping.com/files/processing2.php', files=file)
print(r.text)
```

## 登录
用 `post` 还有一个重要的, 就是模拟登录. 再登录的时候发生了什么事情呢? 我们使用这个简单的登录网页进行说明.
![](https://morvanzhou.github.io/static/results/scraping/3-1-12.png)
通过之前提到的方法, 我们观察一下浏览器给出的记录. 三个重要的方面都被我圈出来了.
![](https://morvanzhou.github.io/static/results/scraping/3-1-13.png)
我们总结一下, 为了这次登录账号, 我们的浏览器做了什么.
1. 使用 post 方法登录了第一个红框的 url
2. post 的时候, 使用了 Form data 中的用户名和密码
3. 生成了一些 cookies

第三点我们是从来没有提到过的. cookie, 听起来很熟呀! 每当游览器出现问题的时候, 网上的解决方法是不是都有什么清除 cookie 之类的, 那 cookie 实际上是什么呢? 这里给出了和全面的介绍.

简单来说, 因为打开网页时, 每一个页面都是不连续的, 没有关联的, cookies 就是用来衔接一个页面和另一个页面的关系. 比如说当我登录以后, 浏览器为了保存我的登录信息, 将这些信息存放在了 cookie 中. 然后我访问第二个页面的时候, 保存的 cookie 被调用, 服务器知道我之前做了什么, 浏览了些什么. 像你在网上看到的广告, 为什么都可能是你感兴趣的商品? 你登录淘宝, 给你推荐的为什么都和你买过的类似? 都是 cookies 的功劳, 让服务器知道你的个性化需求.

所以大部分时候, 每次你登录, 你就会有一个 cookies, 里面会提到你已经是登录状态了. 所以 cookie 在这时候很重要. cookies 的传递也特别重要, 比如我用 `requests.post` + `payload` 的用户信息发给网页, 返回的 `r` 里面会有生成的 cookies 信息. 接着我请求去登录后的页面时, 使用 `request.get`, 并将之前的 cookies 传入到 get 请求. 这样就能已登录的名义访问 get 的页面了.

```python
payload = {'username': 'Morvan', 'password': 'password'}
r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
print(r.cookies.get_dict())

# {'username': 'Morvan', 'loggedin': '1'}


r = requests.get('http://pythonscraping.com/pages/cookies/profile.php', cookies=r.cookies)
print(r.text)

# Hey Morvan! Looks like you're still logged into the site!
```
![](https://morvanzhou.github.io/static/results/scraping/3-1-14.png)
## 使用 Session 登录
不过每次都要传递 cookies 是很麻烦的, 好在 requests 有个很 handy 的功能, 那就是 Session. 在一次会话中, 我们的 cookies 信息都是相连通的, 它自动帮我们传递这些 cookies 信息. 这时我感叹, 程序员真会偷懒~ 哈哈.

同样是执行上面的登录操作, 下面就是使用 session 的版本. 创建完一个 session 过后, 我们直接只用 session 来 `post` 和 `get`. 而且这次 `get` 的时候, 我们并没有传入 cookies. 但是实际上 session 内部就已经有了之前的 cookies 了.

```python
session = requests.Session()
payload = {'username': 'Morvan', 'password': 'password'}
r = session.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
print(r.cookies.get_dict())

# {'username': 'Morvan', 'loggedin': '1'}


r = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(r.text)

# Hey Morvan! Looks like you're still logged into the site!
``` 
# 下载文件
## 使用 urlretrieve
在 urllib 模块中, 提供了我们一个下载功能 urlretrieve. 使用起来很简单. 输入下载地址 IMAGE_URL 和要存放的位置. 图片就会被自动下载过去了.

```python
import os
from urllib.request import urlretrieve
os.makedirs('./img/', exist_ok=True)

IMAGE_URL = "https://morvanzhou.github.io/static/img/description/learning_step_flowchart.png"
urlretrieve(IMAGE_URL, './img/image1.png')
```

## 使用 request
而在 requests 模块, 也能拿来下东西. 下面的代码实现了和上面一样的功能, 但是稍微长了点. 但我们为什么要提到 requests 的下载呢? 因为使用它的另一种方法, 我们可以更加有效率的下载大文件.

```python
import requests
r = requests.get(IMAGE_URL)
with open('./img/image2.png', 'wb') as f:
    f.write(r.content)
```
所以说, 如果你要下载的是大文件, 比如视频等. requests 能让你下一点, 保存一点, 而不是要全部下载完才能保存去另外的地方. 这就是一个 chunk 一个 chunk 的下载. 使用 r.iter_content(chunk_size) 来控制每个 chunk 的大小, 然后在文件中写入这个 chunk 大小的数据.

```python
r = requests.get(IMAGE_URL, stream=True)    # stream loading

with open('./img/image3.png', 'wb') as f:
    for chunk in r.iter_content(chunk_size=32):
        f.write(chunk)
```

# 小练习: 下载美图
## 找到图片位置
说白了, 每次的爬虫, 都是先分析一下这个网页要找的东西的位置, 然后怎么索引上这个位置, 最后用 python 找到它. 这次也是这个逻辑. 我们看看今天要爬的这个图片网址. 定位到最新图片的位置,
![](https://morvanzhou.github.io/static/results/scraping/3-3-2.png)
找到这张图片的所在位置, 对比这类型的图片, 找到一种手段来筛选这些图片. 发现他们都存在于 img_list 的这种 `<ul>` 中.
![](https://morvanzhou.github.io/static/results/scraping/3-3-3.png)
而图片地址都是在 `<img>` 中.

```html
<img src="http://image.nationalgeographic.com.cn/2017/1228/20171228030617696.jpg">
```
现在我们有了思路, 先找带有 img_list 的这种 `<ul>`, 然后在 `<ul>` 里面找 `<img>`.
## 下载图片
有了思路, 现在我们就用 python 来下图吧. import BeautifulSoup 和 requests. 定义爬取的 url.

```python
from bs4 import BeautifulSoup
import requests

URL = "http://www.nationalgeographic.com.cn/animals/"
```
用 BeautifulSoup 找到带有 img_list 的这种 `<ul>`,

```python
html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')
img_ul = soup.find_all('ul', {"class": "img_list"})
```
从 ul 中找到所有的 `<img>`, 然后提取 `<img>` 的 `src` 属性, 里面的就是图片的网址啦. 接着, 就用之前在 `requests` 下载那节内容里提到的一段段下载.

```python
for ul in img_ul:
    imgs = ul.find_all('img')
    for img in imgs:
        url = img['src']
        r = requests.get(url, stream=True)
        image_name = url.split('/')[-1]
        with open('./img/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
```

# 加速爬虫: 多进程分布式
## 什么是分布式爬虫
分布式爬虫主要是为了非常有效率的抓取网页, 我们的程序一般是单线程跑的, 指令也是一条条处理的, 每执行完一条指令才能跳到下一条. 那么在爬虫的世界里, 这里存在着一个问题.

如果你已经顺利地执行过了前几节的爬虫代码, 你会发现, 有时候代码运行的时间大部分都花在了下载网页上. 有时候不到一秒能下载好一张网页的 HTML, 有时候却要几十秒. 而且非要等到 HTML 下载好了以后, 才能执行网页分析等步骤. 这非常浪费时间.

如果我们能合理利用计算资源, 在下载一部分网页的时候就已经开始分析另一部分网页了. 这将会大大节省整个程序的运行时间. 又或者, 我们能同时下载多个网页, 同时分析多个网页, 这样就有种事倍功半的效用. 分布式爬虫的体系有很多种, 处理优化的问题也是多样的. 这里有[一篇博客](http://bittiger.blogspot.com/2016/02/blog-post_3.html)可以当做扩展阅读, 来了解当今比较流行的分布式爬虫框架.
## 我们的分布式爬虫
而今天我们想搭建的这一个爬虫, 就是同时下载, 同时分析的这一种类型的分布式爬虫. 虽然算不上特别优化的框架, 但是概念理解起来比较容易. 我有尝试过徒手写高级一点的分布式爬虫, 但是写起来非常麻烦. 我琢磨了一下, 打算给大家介绍的这种分布式爬虫代码也较好写, 而且效率比普通爬虫快了3.5倍. 我也特地画了张图给大家解释一下要搭建的分布式爬虫.
![](https://morvanzhou.github.io/static/results/scraping/4-1-1.png)
主要来说, 我们最开始有一个网页, 比如说是莫烦Python的首页, 然后首页中有很多 url, 我们使用多进程 ([Python多进程教程](https://morvanzhou.github.io/tutorials/python-basic/multiprocessing/)) 同时开始下载这些 url, 得到这些 url 的 HTML 以后, 同时开始解析 (比如 BeautifulSoup) 网页内容. 在网页中寻找这个网站还没有爬过的链接. 最终爬完整个 莫烦 Python 网站所有页面.

有了这种思路, 我们就可以开始写代码了. 你可以在[我的 Github](https://github.com/MorvanZhou/easy-scraping-tutorial/blob/master/notebook/4-1-distributed-scraping.ipynb) 一次性观看全部代码.

首先 import 全部要用的模块, 并规定一个主页. 注意, 我用这份代码测试我内网的网站(速度不受外网影响) 所以使用的 `base_url` 是 “http://127.0.0.1:4000/”, 如果你要爬 莫烦Python, 你的 `base_url` 要是 “https://morvanzhou.github.io/” (下载速度会受外网影响).

```python
import multiprocessing as mp
import time
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re

# base_url = "http://127.0.0.1:4000/"
base_url = 'https://morvanzhou.github.io/'
```
我们定义两个功能, 一个是用来爬取网页的(crawl), 一个是解析网页的(parse). 有了前几节内容的铺垫, 你应该能一言看懂下面的代码. `crawl()` 用 urlopen 来打开网页, 我用的内网测试, 所以为了体现下载网页的延迟, 添加了一个 `time.sleep(0.1)` 的下载延迟. 返回原始的 HTML 页面, `parse()` 就是在这个 HTML 页面中找到需要的信息, 我们用 BeautifulSoup 找. 返回找到的信息.

```python
def crawl(url):
    response = urlopen(url)
    # time.sleep(0.1)             # slightly delay for downloading
    return response.read().decode()


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])   # 去重
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url
```
网页中爬取中, 肯定会爬到重复的网址, 为了去除掉这些重复, 我们使用 python 的 set 功能. 定义两个 set, 用来搜集爬过的网页和没爬过的.

```python
unseen = set([base_url,])
seen = set()
```

## 测试普通爬法
为了对比效果, 我们将在下面对比普通的爬虫和这种分布式的效果. 如果是普通爬虫, 我简化了一下接下来的代码, 将一些不影响的代码去除掉了, 如果你想看全部的代码, 请来到[我的 Github](https://github.com/MorvanZhou/easy-scraping-tutorial/blob/master/notebook/4-1-distributed-scraping.ipynb). 我们用循环一个个 `crawl` `unseen` 里面的 `url`, 爬出来的 HTML 放到 `parse` 里面去分析得到结果. 接着就是更新 `seen` 和 `unseen` 这两个集合了.

特别注意: 任何网站都是有一个服务器压力的, 如果你爬的过于频繁, 特别是使用多进程爬取或异步爬取, 一次性提交请求给服务器太多次, 这将可能会使得服务器瘫痪, 你可能再也看不到莫烦 Python 了. 所以为了安全起见, 我限制了爬取数量(restricted_crawl=True). 因为我测试使用的是内网 “http://127.0.0.1:4000/” 所以不会有这种压力. 你在以后的爬网页中, 会经常遇到这样的爬取次数的限制 (甚至被封号). 我以前爬 github 时就被限制成一小时只能爬60页.

```PYTHON
# DON'T OVER CRAWL THE WEBSITE OR YOU MAY NEVER VISIT AGAIN
if base_url != "http://127.0.0.1:4000/":
    restricted_crawl = True
else:
    restricted_crawl = False

while len(unseen) != 0:                 # still get some url to visit
    if restricted_crawl and len(seen) >= 20:
        break
    htmls = [crawl(url) for url in unseen]
    results = [parse(html) for html in htmls]

    seen.update(unseen)         # seen the crawled
    unseen.clear()              # nothing unseen

    for title, page_urls, url in results:
        unseen.update(page_urls - seen)     # get new url to crawl
```
使用这种单线程的方法, 在我的内网上面爬, 爬完整个 莫烦Python, 一共消耗 52.3秒. 接着我们把它改成多进程分布式.

## 测试分布式爬法
还是上一个 `while` 循环, 首先我们创建一个进程池(Pool). 不太懂进程池的朋友看过来. 然后我们修改得到 `htmls` 和 `results` 的两句代码. 其他都不变, 只将这两个功能给并行了. 我在这里写的都是简化代码, 你可以在[这里](https://github.com/MorvanZhou/easy-scraping-tutorial/blob/master/notebook/4-1-distributed-scraping.ipynb) 看到完整代码.

```python
pool = mp.Pool(4)
while len(unseen) != 0:
    # htmls = [crawl(url) for url in unseen]
    # --->
    crawl_jobs = [pool.apply_async(crawl, args=(url,)) for url in unseen]
    htmls = [j.get() for j in crawl_jobs]

    # results = [parse(html) for html in htmls]
    # --->
    parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
    results = [j.get() for j in parse_jobs]

    ...
```

# 加速爬虫: 异步加载 Asyncio
Python 还提供了一个有力的工具, 叫做 asyncio. 这是一个仅仅使用单线程, 就能达到多线程/进程的效果的工具. 它的原理, 简单说就是: 在单线程里使用异步计算, 下载网页的时候和处理网页的时候是不连续的, 更有效利用了等待下载的这段时间.
## 基本用法
接着我们来举例介绍 asyncio, 像之前画的图那样, 我们要时刻记住, asyncio 不是多进程, 也不是多线程, 单单是一个线程, 但是是在 Python 的功能间切换着执行. 切换的点用 `await` 来标记, 能够异步的功能用 `async` 标记, 比如 `async def function():`. 首先我们看一下, 不使用 `async` 完成的一份代码, 然后我们将这份代码改成 `async` 版的. 这些代码我都会放在我的 github 中, 如果想一次性看全部, 请来这里.

```pyhton
# 不是异步的
import time


def job(t):
    print('Start job ', t)
    time.sleep(t)               # wait for "t" seconds
    print('Job ', t, ' takes ', t, ' s')


def main():
    [job(t) for t in range(1, 3)]


t1 = time.time()
main()
print("NO async total time : ", time.time() - t1)

"""
Start job  1
Job  1  takes  1  s
Start job  2
Job  2  takes  2  s
NO async total time :  3.008603096008301
"""
```
从上面可以看出, 我们的 job 是按顺序执行的, 必须执行完 `job 1` 才能开始执行 `job 2`, 而且 `job 1` 需要1秒的执行时间, 而 `job 2` 需要2秒. 所以总时间是 3 秒多. 而如果我们使用 asyncio 的形式, `job 1` 在等待 `time.sleep(t)` 结束的时候, 比如是等待一个网页的下载成功, 在这个地方是可以切换给 `job 2`, 让它开始执行.

```python
import asyncio


async def job(t):                   # async 形式的功能
    print('Start job ', t)
    await asyncio.sleep(t)          # 等待 "t" 秒, 期间切换其他任务
    print('Job ', t, ' takes ', t, ' s')


async def main(loop):                       # async 形式的功能
    tasks = [
    loop.create_task(job(t)) for t in range(1, 3)
    ]                                       # 创建任务, 但是不执行
    await asyncio.wait(tasks)               # 执行并等待所有任务完成

t1 = time.time()
loop = asyncio.get_event_loop()             # 建立 loop
loop.run_until_complete(main(loop))         # 执行 loop
loop.close()                                # 关闭 loop
print("Async total time : ", time.time() - t1)

"""
Start job  1
Start job  2
Job  1  takes  1  s
Job  2  takes  2  s
Async total time :  2.001495838165283
"""
```
从结果可以看出, 我们没有等待 `job 1` 的结束才开始 `job 2`, 而是 `job 1` 触发了 `await` 的时候就切换到了 `job 2` 了. 这时, `job 1` 和 `job 2` 同时在等待 `await asyncio.sleep(t)`, 所以最终的程序完成时间, 取决于等待最长的 `t`, 也就是 2秒. 这和上面用普通形式的代码相比(3秒), 的确快了很多.

## aiohttp
有了对 asyncio 的基本了解, 我们就来看怎么把它用在爬虫. 这个功能对于爬虫非常的理想, 原因很简单, 我们在等待一个网页下载的时候, 完全可以切换到其它代码, 事半功倍. 但是 asycio 自己还是没办法完成这项任务的, 我们还需要安装另一个牛逼的模块将 `requests` 模块代替成一个异步的 `requests`, 这个牛逼的模块叫作 `aiohttp` (官网在这). 下载安装特别简单. 直接在你的 terminal 或者 cmd 里面输入 “pip3 install aiohttp”.

接着我们来看看我们怎么用最一般的 requests 模块爬网页, 和我们怎么将 requests 替换成 aiohttp.

```python
import requests

URL = 'https://morvanzhou.github.io/'


def normal():
    for i in range(2):
        r = requests.get(URL)
        url = r.url
        print(url)

t1 = time.time()
normal()
print("Normal total time:", time.time()-t1)

"""
https://morvanzhou.github.io/
https://morvanzhou.github.io/
Normal total time: 0.3869960308074951
"""
```
用 requests 用久了以后, 这样的代码真是信手拈来. 很好, 我们打开 莫烦 Python 的首页两次只花了 0.38秒. 然后我们在用 aiohttp 来实现一样的功能. 结果 asyncio 的方式只用了 0.11秒! 大获全胜.

```python
import aiohttp


async def job(session):
    response = await session.get(URL)       # 等待并切换
    return str(response.url)


async def main(loop):
    async with aiohttp.ClientSession() as session:      # 官网推荐建立 Session 的形式
        tasks = [loop.create_task(job(session)) for _ in range(2)]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]    # 获取所有结果
        print(all_results)

t1 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
print("Async total time:", time.time() - t1)

"""
['https://morvanzhou.github.io/', 'https://morvanzhou.github.io/']
Async total time: 0.11447715759277344
"""
```
我们刚刚创建了一个 Session, 这是官网推荐的方式, 但是我觉得也可以直接用 request 形式, 细节请参考官方说明. 如果要获取网页返回的结果, 我们可以在 `job()` 中 return 个结果出来, 然后再在 `finished, unfinished = await asyncio.wait(tasks)` 收集完成的结果, 这里它会返回完成的和没完成的, 我们关心的都是完成的, 而且 `await` 也确实是等待都完成了才返回. 真正的结果被存放在了 `result()` 里面.
## 和多进程分布式爬虫对比
有了这些基础, 我们就可以来玩点高级的了, 之前我们用 `multiprocessing` 写过了一个简单的分布式爬虫, 现在我们就来拿过来 PK 一下 asyncio 的方法. 首先我们对比一下这次写的结构和上次写的简单分布式爬虫的区别. 分布式我们完全依赖的是 multiprocessing 这个模块. 不了解的可以快速过一遍这个教程. 使用 python 强大的并行处理运算来下载我们要处理的 urls, 然后解析网页也是一件耗时的事, 特别是网页量多的时候. 所以我们也将网页解析给并行了. 这样大大节省了下载和运算时间. 再看右边的这个 asyncio 的例子, 我们解析网页还是用的和 multiprocessing 那边一样的并行处理, 因为 asyncio 好像不支持解析网页的异步, 毕竟是计算密集型工序. 然后不一样的地方是, 我们在下载网页时, 不用 multiprocessing, 改用 asyncio, 用一个单线程的东西挑战多进程.
![](https://morvanzhou.github.io/static/results/scraping/4-2-3.png)

```python
import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
import re
import multiprocessing as mp

# base_url = "https://morvanzhou.github.io/"
base_url = "http://127.0.0.1:4000/"

# DON'T OVER CRAWL THE WEBSITE OR YOU MAY NEVER VISIT AGAIN
if base_url != "http://127.0.0.1:4000/":
    restricted_crawl = True
else:
    restricted_crawl = False

seen = set()
unseen = set([base_url])


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url


async def crawl(url, session):
    r = await session.get(url)
    html = await r.text()
    await asyncio.sleep(0.1)  # slightly delay for downloading
    return html


async def main(loop):
    pool = mp.Pool(8)  # slightly affected
    async with aiohttp.ClientSession() as session:
        count = 1
        while len(unseen) != 0:
            print('\nAsync Crawling...')
            tasks = [loop.create_task(crawl(url, session)) for url in unseen]
            finished, unfinished = await asyncio.wait(tasks)
            htmls = [f.result() for f in finished]

            print('\nDistributed Parsing...')
            parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
            results = [j.get() for j in parse_jobs]

            print('\nAnalysing...')
            seen.update(unseen)
            unseen.clear()
            for title, page_urls, url in results:
                # print(count, title, url)
                unseen.update(page_urls - seen)
                count += 1


if __name__ == "__main__":
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    # loop.close()
    print("Async total time: ", time.time() - t1)
```
# 高级爬虫: 让 Selenium 控制你的浏览器帮你爬
## 安装 Selenium
因为 Selenium 需要操控你的浏览器, 所以安装起来比传统的 Python 模块要多几步. 先在 terminal 或者 cmd 用 pip 安装 selenium.

```shell
# python 2+
pip install selenium

# python 3+
pip3 install selenium
```
要操控浏览器, 你就要有浏览器的 driver. Selenium 针对几个主流的浏览器都有 driver. 针对 Linux 和 MacOS.

* Chrome [driver](https://sites.google.com/a/chromium.org/chromedriver/downloads), 如果前面链接无法打开, 请尝试这个, 并下载对应版本的 driver
* Edge driver
* Firefox driver
* Safari driver
Linux 和 MacOS 用户下载好之后, 请将下载好的”geckodriver”文件放在你的计算机的 “/usr/bin” 或 “/usr/local/bin” 目录. 并赋予执行权限, 不会放的, 请使用这条语句.

## Python 控制浏览器
好了, 有了这些代码, 我们就能回到 Python. 开始写 Python 的代码了. 这里十分简单! 我将 selenium 绑定到 Chrome 上 `webdriver.Chrome()`. 你可以绑其它的浏览器.

```python
from selenium import webdriver

driver = webdriver.Chrome()     # 打开 Chrome 浏览器

# 将刚刚复制的帖在这
# driver.get("https://morvanzhou.github.io/")
# driver.find_element_by_xpath(u"//img[@alt='强化学习 (Reinforcement Learning)']").click()
# driver.find_element_by_link_text("About").click()
# driver.find_element_by_link_text(u"赞助").click()
# driver.find_element_by_link_text(u"教程 ▾").click()
# driver.find_element_by_link_text(u"数据处理 ▾").click()
# driver.find_element_by_link_text(u"网页爬虫").click()

driver.get("https://www.baidu.com/")

# 得到网页 html, 还能截图
html = driver.page_source       # get html
driver.get_screenshot_as_file("./img/sreenshot1.png")
driver.close()

```
我们能得到页面的 html code (`driver.page_source`), 就能基于这个 code 来爬取数据了. 最后爬取的网页截图就是这样.
不过每次都要看着浏览器执行这些操作, 有时候有点不方便. 我们可以让 selenium 不弹出浏览器窗口, 让它”安静”地执行操作. 在创建 driver 之前定义几个参数就能摆脱浏览器的身体了.

```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")       # define headless

driver = webdriver.Chrome(chrome_options=chrome_options)
```
Selenium 能做的事还有很多, 比如填 Form 表单, 超控键盘等等. 这个教程不会细说了, 只是个入门, 如果你还想继续深入了解, 欢迎点进去他们的 [Python 教学官网](http://selenium-python.readthedocs.io/).

最后, Selenium 的优点我们都看出来了, 可以很方便的帮你模拟你的操作, 添加其它操作也是非常容易的, 但是也是有缺点的, 不是任何时候 selenium 都很好. 因为要打开浏览器, 加载更多东西, 它的执行速度肯定没有其它模块快. 所以如果你需要速度, 能不用 Selenium, 就不用吧.

# 高级爬虫: 高效无忧的 Scrapy 爬虫库
## Scrapy 的优势
Scrapy 是一个整合了的爬虫框架, 有着非常健全的管理系统. 而且它也是分布式爬虫, 但是比我们之前写的那个分布式爬虫高级多了. 下面就是 Scrapy 的框架示意图(来源). 它的管理体系非常复杂. 但是特别高效. 让你又刷网页, 又下载, 同时能处理数据. 简直千手观音呀.
![](https://morvanzhou.github.io/static/results/scraping/5-2-2.png)
## Scrapy 爬虫
好了, 我们开始今天的简单 Scrapy 教程吧. 首先你得安装 Scrapy. 在 terminal 或者 cmd 使用 pip 安装就好.

```shell
# python 2+
pip install scrapy

# python 3+
pip3 install scrapy
```
我们之前有做过爬取 莫烦Python 全网的信息. 用`多进程` 和`异步爬取`都做过. 这次, 我们就用 Scrapy 来实现这样的一个爬虫. 剧透一下, 做前两个的时候, 代码行数差不多都是 50+ 行, 但是 scrapy 只需要用 20+ 行代码就解决的上面的事. 哈哈, 功能强大吧.

我们导入 scrapy 模块, 并创建一个 spider 的 class. 并继承 `scrapy.Spider`, 一定还要给这个 spider 一个名字, 我就用 `mofan` 好了, 因为是爬 莫烦Python 的. 给定一些初始爬取的网页, 写在 `start_urls` 里. 这里特别要提的是: 之前我们用 python 的 set 来去除重复的 url, 在 scrapy 中, 这是不需要的, 因为它自动帮你去重. 这可省心多了. 如果你想一次性看到全部代码, 请看到[我的 github](https://github.com/MorvanZhou/easy-scraping-tutorial/blob/master/notebook/5-2-scrapy.ipynb).

```python
import scrapy

class MofanSpider(scrapy.Spider):
    name = "mofan"
    start_urls = [
        'https://morvanzhou.github.io/',
    ]
    # unseen = set()
    # seen = set()      # 我们不在需要 set 了, 它自动去重
```
接着我们还要定义这个 class 中的一个功能就能完事了. 我们使用 python 的 yield 来返回搜集到的数据 (为什么是yield? 因为在 scrapy 中也有异步处理, 加速整体效率). 这些 title 和 url 的数据, 我们都是用 scrapy 中抓取信息的方式.

```python
class MofanSpider(scrapy.Spider):
    ...
    def parse(self, response):
        yield {     # return some results
            'title': response.css('h1::text').extract_first(default='Missing').strip().replace('"', ""),
            'url': response.url,
        }

        urls = response.css('a::attr(href)').re(r'^/.+?/$')     # find all sub urls
        for url in urls:
            yield response.follow(url, callback=self.parse)     # it will filter duplication automatically
```
然后在这个response网页中筛选 `urls`, 这里我们也不需要使用 `urljoin()` 这种功能给 url 改变形式. 它在 `follow()` 这一步会自动检测 url 的格式. (真是省心啊~), 然后对于每个找到的 url, 然后 yield 重新使用 `self.parse()` 来爬取, 这里又是自动去重! Scrapy 仿佛知道你最不想做什么, 它自动帮你都做好了. 开心~

最后需要运行的时候有点不同, 你需要在 terminal 或 cmd 中运行这个爬虫. 而且还能帮你保存刚刚 yield 的 `{title:, url:}` 的结果. `runspider 5-2-scrapy.py` 就是选择你要跑的这个 Python 文件.

```shell
$ scrapy runspider 5-2-scrapy.py -o res.json
```
`-o res.json` 这个 `-o` 就是输出的指令, 你可以在那个文件夹中找到一个名字叫 `res.json` 的文件, 里面存有所有找到的 `{title:, url:}`.
# 附录
[正则表达式基础教程](https://morvanzhou.github.io/tutorials/python-basic/basic/13-10-regular-expression/)
![小超](https://morvanzhou.github.io/static/results/basic/13-10-01.png)