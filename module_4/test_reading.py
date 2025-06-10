import pytest

def format_data_for_display(people:list[dict]) -> list[str]:

    return [
        f"{p['given_name']} {p['family_name']}: {p['title']}"\
        for p in people
    ]
    



def test_format_data_for_display():
    people = [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]

    assert format_data_for_display(people) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]