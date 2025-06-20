import urllib3
from urllib.parse import urljoin
from urllib import robotparser
from bs4 import BeautifulSoup

def _get_robots_txt(agent:str, url:str, paths:list[str]) -> dict[str, bool]:
    """Fetches the robots.txt file for the given URL and checks if the provided
    paths are allowed for the given user agent.
    """
    # Create a robot parser and set the URL to robots.txt file
    parser = robotparser.RobotFileParser(url)
    parser.set_url(urljoin(url, "robots.txt"))
    parser.read()

    allowed_paths = {}
    for path in paths:
        allowed_paths[path] = parser.can_fetch(agent, path)

    return allowed_paths

def _parse_column_titles(soup:BeautifulSoup) -> list[str]:
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

def _parse_rows(soup:BeautifulSoup) -> list[list[str]]:
    """Extract rows of data from the survey page. This will result in
    duplicate 'Accepted/Failed on ##' entries that must be cleaned."""
    working_list = []
    results = []

    # tbody contains tr elements with data rows.
    # Survey results are broken into 3 rows; first row has no class,
    # second row will be there and is comprised of divs, third row
    # may be there and is comprised of a p element.
    tbody = soup.find("tbody")
    tr_iter = tbody.find_all("tr")
    for tr in tr_iter:
        # First line of result:
        if "class" not in tr.attrs.keys():
            # Append list to results and create new
            if working_list:
                results.append(working_list)
                working_list = []
            
            # Find column data and append
            for col_i, col in enumerate(tr.find_all("td")):
                # First four columns are text, the 5th has a link to the survey page
                if col_i < 4:
                    working_list.append(col.text.strip())
                else:
                    working_list.append(col.find("a").attrs['href'])

        # Second or third line of result:          
        else:
            for col in tr.find_all("div", class_="tw-inline-flex"):  # Second line
                working_list.append(col.text.strip())
            for col in tr.find_all("p"):  # Third line
                working_list.append(col.text.strip())

    if working_list:
        results.append(working_list)
    
    return results

def scrape_data(agent:str, url:str, paths:list[str], min_results:int=10000, max_pages_to_crawl:int=10000,
                starting_page:int=1) -> tuple[list, list[list[str]]]:
    """Scrape survey data from the GradCafe website."""
    # Fetch robots.txt and check availabilty of paths
    allowed_paths = _get_robots_txt(agent, url, paths)
    for path in allowed_paths:
        if not allowed_paths[path]:
            print(f"Path {path} is not allowed for user agent '{agent}'")

    results = []
    page_number = starting_page
    n_pages_crawled = 0
    n_surveys = 0

    http = urllib3.PoolManager()

    while (n_surveys <= min_results) and (n_pages_crawled < max_pages_to_crawl):
        # Construct the URL for the current page
        page_url = f"{url}?page={page_number}"

        if page_number % 10 == 0:
            print(f"{n_surveys} / {min_results} results found, crawling page {page_number} / {max_pages_to_crawl} maximum...")

        # Fetch the page content
        try:
            response = http.request('GET', page_url)
            soup = BeautifulSoup(response.data, "html.parser")
        except Exception as e:
            print(f"Failed to fetch {page_url}: {e}")
            break

        # Parse column titles and rows
        if page_number == starting_page:
            column_titles = _parse_column_titles(soup)

        rows = _parse_rows(soup)
        results.extend(rows)

        n_surveys = len(results)
        n_pages_crawled += 1
        page_number += 1

    return column_titles, results