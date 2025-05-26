from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/poseidon"

page = urlopen(url)
html = page.read().decode("utf-8")

pat = re.compile(r'<.*title.*>(.*?)</.*title.*>', re.IGNORECASE)
match = pat.search(html)
print(match)