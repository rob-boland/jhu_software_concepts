from urllib import parse, robotparser
from urllib.request import urlopen
from bs4 import BeautifulSoup

agent = "rob"
url = "https://www.thegradcafe.com/"
survey_url = f"{url}survey/"

def get_robots_txt(url:str, paths:list[str]) -> dict[str, bool]:
    """Fetches the robots.txt file for the given URL and checks if the provided
    paths are allowed for the given user agent.
    """
    # Create a robot parser and set the URL to robots.txt file
    parser = robotparser.RobotFileParser(url)
    parser.set_url(parse.urljoin(url, "robots.txt"))
    parser.read()

    allowed_paths = {}
    for path in paths:
        allowed_paths[path] = parser.can_fetch(agent, path)

    return allowed_paths

paths = ["/", "/survey/"]

survey_page = urlopen(survey_url)
html = survey_page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

def parse_column_titles(soup:BeautifulSoup) -> list[str]:
    """Extract column titles from the survey page."""
    column_titles = []

    # thead contains tr which contains th elements with column titles
    thead = soup.find("thead")
    tr = thead.find("tr")
    if tr:
        for th in tr.find_all("th"):
            col_title_raw = th.get_text(strip=True)
            col_title_formatted = col_title_raw.replace(" ", "_").lower()
            if "sort" not in col_title_formatted:
                column_titles.append(col_title_formatted)
    
    return column_titles

tbody = soup.find("tbody")
tr = tbody.find_all("tr")
for row in tr:
    if "class" not in row.attrs.keys():  # First line of result
        for col in row.find_all("td")[:4]:
            print(col.text.strip())
        print("-" * 20)