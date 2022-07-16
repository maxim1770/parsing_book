import re

import requests


def get_title_book_eng_for_link(link):


    regex = r"(?<=material\/).*"
    Match = re.search(regex, link)

    try:
        return Match.group()
    except AttributeError as err:
        return None



def main():

    pass

if __name__ == "__main__":
    main()