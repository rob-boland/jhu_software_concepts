import json
import re

with open("module_2/data/survey_data_working.json", "r") as f:  
    data = json.load(f)

column_titles, results = data
print("Column Titles:")
for title in column_titles:
    print(title)
# print("\nResults:")
# for row in results:
#     print(row)

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

x = _separate_program_name_from_level("Mechanical And Aerospace EngineeringMasters")

print(x)