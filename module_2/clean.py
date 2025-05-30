import json
import re
import datetime

with open("module_2/data/survey_data_working.json", "r") as f:  
    data = json.load(f)

column_titles, results = data

categories = {
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
    # GRE and GPA scores follow a spccific format. Anything else is considered a comment.
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

    return update_dict

if __name__ == "__main__":
    agent = "rob"
    url = "https://www.thegradcafe.com/"
    survey_url = f"{url}survey/"
    paths = ["/", "/survey/"]

    cleaned_results = []
    for result in results:
        try:
            result_dict = {k:None for k in categories}
            result_dict["university"] = result[0]
            result_dict["program_name"], result_dict["program_level"] = _separate_program_name_from_level(result[1])
            result_dict["date_of_information_added"] = datetime.datetime.strptime(result[2], "%b %d, %Y")
            result_dict["applicant_status"] = result[3]
            result_dict["url_link"] = f"{url}{result[4][1:]}"  # Remove leading slash
            result_dict["program_start_semester"] = result[6]
            result_dict["nationality"] = result[7]

            # If GRE, GPA, or comments are present, update dictionary
            if len(result) > 8:
                result_dict.update(_clean_secondary_rows(result[8:]))
            
            cleaned_results.append(result_dict)

        except IndexError as e:
            print("Improperly formatted result:", result)
            continue
