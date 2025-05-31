import json
import re
import datetime

from scraper import scrape_data

_categories = {
    "university",
    "program_name",
    "program_level",
    "applicant_status",
    "date_of_information_added",
    "url_link",
    "program_start_semester",
    "nationality",
    "gre_score",
    "gre_v_score",
    "gre_aw_score",
    "gpa",
    "comments"
}

def _separate_program_name_from_level(program_name_and_level:str) -> tuple[str, str]:
    """Separate program level from program name. Expects a string with a newline character
    separating name from level, but can also use regex to find common degrees."""

    if "\n" in program_name_and_level:
        parts = program_name_and_level.split("\n")
        return (parts[0], parts[-1])
    else:
        regex = r"(PhD|Masters|MFA|MBA|JD|EdD|Other|PsyD)"
        match = re.search(regex, program_name_and_level, flags=re.IGNORECASE)
        if match:
            name = program_name_and_level[:match.start()].strip()
            degree = match.group(0)
            return (name, degree)
        else:
            return (program_name_and_level, "")

def _clean_secondary_rows(row_data:list[str]) -> dict:
    """Clean GPA, GRE, and comments data from secondary rows."""

    update_dict = {}
    # GRE and GPA scores follow a specific format. Anything else is considered a comment.

    try:
        for datum in row_data:
            if datum[:3] == "GRE":
                if "AW" in datum:
                    update_dict["gre_aw_score"] = float(re.search(r"\d+.\d+", datum).group(0))
                elif "V" in datum:
                    update_dict["gre_v_score"] = int(re.search(r"\d+", datum).group(0))
                else:
                    update_dict["gre_score"] = int(re.search(r"\d+", datum).group(0))

            elif datum[:3] == "GPA":
                update_dict["gpa"] = float(re.search(r"\d+.\d+", datum).group(0))

            else:
                update_dict["comments"] = datum
    except AttributeError as e:
        # If regex fails to find a match, skip that datum
        pass

    return update_dict

def _convert_date_to_iso(date_str:str) -> tuple[str, int]:
    """Convert date string to ISO format (YYYY-MM-DD). Returns a tuple of the date in
    ISO format and the year."""
    try:
        date_obj = datetime.datetime.strptime(date_str, "%b %d, %Y")
        return (date_obj.strftime("%Y-%m-%d"), date_obj.year)
    except ValueError:
        return (date_str, datetime.date.today().year)  # Return original string if conversion fails
    
def _clean_applicant_status(full_status_str:str, year:int) -> str:
    """Clean applicant status string to a standardized format."""
    full_status_str = full_status_str.lower()
    if "accept" in full_status_str:
        status = "Accepted"
    elif "reject" in full_status_str:
        status = "Rejected"
    elif "wait" in full_status_str:
        status = "Waitlisted"
    elif "interview" in full_status_str:
        status = "Interviewed"
    else:
        status = "Other"
    
    day_month_of_decision = re.search(r"\d{1,2} \w{3}", full_status_str).group(0) + f" {str(year)}"
    datetime_of_decision = datetime.datetime.strptime(day_month_of_decision, "%d %b %Y")

    return (status, datetime_of_decision.strftime("%Y-%m-%d"))

def save_data(data:list[dict], filename:str) -> None:
    """Save the cleaned data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    return None

def load_data(filename:str) -> list[dict]:
    """Load the cleaned data from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def clean_data(agent:str, url:str, paths:list[str], min_results:int=10000, max_pages_to_crawl:int=10000,
               starting_page:int=1) -> list[dict]:
    """Clean data scraped from the provided URL and paths, returning a list of dictionaries."""
    
    # Scrape data, separate into column titles and results
    parsed_data = scrape_data(
        agent=agent,
        url=url,
        paths=paths,
        min_results=min_results,
        max_pages_to_crawl=max_pages_to_crawl,
        starting_page=starting_page
    )
    column_titles, results = parsed_data

    # Build a dictionary for each result with standardized keys
    cleaned_results = []
    for result in results:
        try:
            result_dict = {k:None for k in _categories}
            result_dict["university"] = result[0]
            result_dict["program_name"], result_dict["program_level"] = _separate_program_name_from_level(result[1])
            result_dict["date_of_information_added"], year = _convert_date_to_iso(result[2])
            result_dict["applicant_status"] = _clean_applicant_status(result[3], year)
            result_dict["url_link"] = f"{url}{result[4][1:]}"  # Remove leading slash
            result_dict["program_start_semester"] = result[6]
            result_dict["nationality"] = result[7]

            # If GRE, GPA, or comments are present, update dictionary, else keep None
            if len(result) > 8:
                result_dict.update(_clean_secondary_rows(result[8:]))
            
            cleaned_results.append(result_dict)

        except IndexError as e:
            # Improperly formatted row, potentially missing data. Ignore
            continue
    
    return cleaned_results

if __name__ == "__main__":
    cleaned_data = clean_data(
        agent="rob",
        url="https://www.thegradcafe.com/survey/",
        paths=["/", "/survey/"],
        min_results=5000,
        max_pages_to_crawl=5000
    )

    save_data(cleaned_data, "module_2/visible_data/cleaned_survey_data.json")
