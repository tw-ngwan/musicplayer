import sqlite3


def input_parse(name="links", function="download") -> list[str]:
    names_string = input(f"Copy the {name} you want to {function}, separated by a space \n")
    names = names_string.split()
    print(f"Added all {names}")
    return names
