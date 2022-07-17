import re

import requests


def get_title_book_eng_for_link(link):
    regex = r"(?<=material\/).*"
    Match = re.search(regex, link)

    try:
        return Match.group()
    except AttributeError as attribute_err:
        print("[my_ERROR] ошибка поиска имени в пути https://../title_book_eng_for_link нужно было получить title_book_eng_for_link")
        raise attribute_err
        # return None


def get_file_name_not_extension(file_name):
    regex = r".*(?=\.)"
    Match = re.search(regex, file_name)

    try:
        return Match.group()
    except AttributeError as attribute_err:
        print("[my_ERROR] ошибка поиска имени файла title_book_eng_for_link.html")
        raise attribute_err
        # return None

def edit_title(title:str):
    regex = r".*"
    Match = re.search(regex, title)

    try:
        return Match.group()
    except AttributeError as attribute_err:
        raise attribute_err


def edit_date(date:str):
    regex = r".*"
    Match = re.search(regex, date)

    try:
        return Match.group()
    except AttributeError as attribute_err:
        raise attribute_err


def edit_sheets_number_to_int(sheets_number_str):
    regex = r"\d+"
    Match = re.search(regex, sheets_number_str)

    try:
        sheets_number_int = int(Match.group())
        return sheets_number_int
    except AttributeError as attribute_err:
        print("[my_ERROR] Не нашлось чисел в строке 'объем листов'")
        raise attribute_err
        # return None

def edit_owner(owner:str):
    regex = r".*"
    Match = re.search(regex, owner)

    try:
        return Match.group()
    except AttributeError as attribute_err:
        raise attribute_err


def main():
    pass


if __name__ == "__main__":
    main()
