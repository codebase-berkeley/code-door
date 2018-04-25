from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

req = Request('https://www.glassdoor.com/index.htm', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

soup = BeautifulSoup(html)

print(soup.prettify())
print(soup.find_all('a'))
