from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/aphrodite"

page = urlopen(url)
html = page.read().decode("utf-8")
print(html)