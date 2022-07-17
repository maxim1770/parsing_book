import os
import datetime
import time
import json
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import re


def check_have_good_date(date: str):
    # if re.search(r"[XV]", data):
    #     print(data)

    regex = r"(?:(?<![XIV])XI*V?I?(?![XIV]))|(?:(?:(?<!\d)1[0-5]\d\d(?!\d))|(?:(?<!\d)\d\d\d(?!\d)))"
    Match = re.search(regex, date)

    if Match:
        print(Match.group())
        return True
    else:
        return False


def check_have_bad_date(date):
    regex = r"(?:(?<![XIV])(?:(?:XVI{2,3})|(?:XI?XI?))(?![XIV]))|(?:(?<!\d)1[6-9]\d\d(?!\d))"
    Match = re.search(regex, date)

    if Match:
        print("Группа maybe", Match.group())
        return True
    else:
        return False


def get_datas_descriptions_sections(headers):
    pages_html = os.listdir('data/pages_books')

    datas_descriptions_sections_page = set()

    # ---
    count_iteration = 0
    # ---
    for page_html in pages_html:
        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {page_html}")
        # ---

        with open(f"data/pages_books/{page_html}", encoding='utf-8') as file:
            src = file.read()

        data_descriptions_sections_page = get_data_descriptions_section_page(src=src)

        # ---
        print(f"Данные: {data_descriptions_sections_page}")
        print(
            f"Новые данные (не было их раньше): {data_descriptions_sections_page.difference(datas_descriptions_sections_page)}")
        print('-' * 20)
        # ---

        datas_descriptions_sections_page = datas_descriptions_sections_page.union(data_descriptions_sections_page)
        # ---
        count_iteration += 1
        # ---
    return datas_descriptions_sections_page


def get_data_descriptions_section_page(src):
    soup = BeautifulSoup(src, "lxml")

    # table_info = soup.find("h3", text=re.compile("Сведения о документе")).find_parent('div', class_="book-info")
    # rows_info = table_info.find_all('div', class_="book-info-table")

    owner = soup.find('div', text=re.compile(r"Владелец")).find_next_sibling('div').text.strip()
    data_descriptions_sections_page = {owner, }
    return data_descriptions_sections_page


def main():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36",
    }

    datas_descriptions_sections = get_datas_descriptions_sections(headers)
    datas_descriptions_sections = list(datas_descriptions_sections)
    # ---
    print(f"Общее кол. данных раздела: {len(datas_descriptions_sections)}")
    print(datas_descriptions_sections)
    # ---


if __name__ == "__main__":
    main()
