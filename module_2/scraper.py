from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://olympus.realpython.org/profiles/dionysus"

page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

print(soup.title.sourceline)