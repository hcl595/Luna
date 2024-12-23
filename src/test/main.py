from bs4 import BeautifulSoup
import urllib.request

url = "http://www.baidu.com"
response1 = urllib.request.urlopen(url)
html = response1.read()
soup = BeautifulSoup(html, 'html.parser')

codes = soup.find_all('code')
for code in codes:
    print(code.text)
