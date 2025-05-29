from urllib import parse, robotparser

agent = "rob"
url = "https://www.thegradcafe.com/"

def get_robots_txt(url:str, paths:list[str]) -> list[tuple[bool, str]]:
    """Fetches the robots.txt file for the given URL and checks if the provided
    paths are allowed for the given user agent.
    """
    # Create a robot parser and set the URL to robots.txt file
    parser = robotparser.RobotFileParser(url)
    parser.set_url(parse.urljoin(url, "robots.txt"))
    parser.read()

    allowed_paths = []
    for path in paths:
        allowed_paths.append(f"{parser.can_fetch(agent, path), path}")

    return allowed_paths

print(get_robots_txt(url))

paths = [
        "/",
        "/cgi-bin/",
        "/admin/",
        "survey/?program=Computer+Science"
    ]