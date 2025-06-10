import pytest

def is_palindrome(str_:str) -> bool:

    condensed_str = ""
    for char in str_:
        if char.isalpha():
            condensed_str += char.lower()

    reversed_str = ""
    for i in range(len(condensed_str) - 1, -1, -1):
        reversed_str += condensed_str[i]
    return condensed_str == reversed_str


@pytest.mark.parametrize("palindrome", [
    "",
    "a",
    "Bob",
    "Never odd or even",
    "Do geese see God?"
])
def test_is_palindrome(palindrome):
    assert is_palindrome(palindrome)
