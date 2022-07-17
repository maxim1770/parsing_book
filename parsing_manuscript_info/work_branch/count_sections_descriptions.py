import os
import datetime
import time
import json
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import re


# import getpagedat

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


def write_file_links_pages(url, headers):
    # req = requests.get(url, headers)
    #
    # with open('data/main_page.html', "w", encoding="utf-8") as file:
    #     file.write(req.text)

    links_pages_true = []
    links_pages_maybe = []

    with open('data/main_page.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    cards = soup.find_all('div', class_='content-tile')

    for card in cards:
        link = card.find("a")
        date = link.find('p').text
        if not check_have_good_date(date):
            continue

        title = link.find('h3').text
        href = "https://kp.rusneb.ru" + link["href"]

        if check_have_bad_date(date):
            links_pages_maybe.append(
                {
                    "title": title,
                    "date": date,
                    "link": href,
                }
            )
        else:
            links_pages_true.append(
                {
                    "title": title,
                    "date": date,
                    "link": href,
                }
            )

    with open("data/folder_links_pages/links_pages_true.json", "w", encoding="utf-8") as file:
        json.dump(links_pages_true, file, indent=4, ensure_ascii=False)

    with open("data/folder_links_pages/links_pages_maybe.json", "w", encoding="utf-8") as file:
        json.dump(links_pages_maybe, file, indent=4, ensure_ascii=False)


def get_count_descriptions_sections(headers):
    with open('data/links_pages.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    descriptions_sections = set()

    # ---
    count_iteration = 0
    # ---
    for link_content in data:
        req = requests.get(link_content["link"], headers)

        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {link_content['title']}")
        # ---

        descriptions_sections_page = get_descriptions_sections_page(src=req.text)

        # ---
        print(f"Разделы: {descriptions_sections_page}")
        print(f"Новые разделы (не было их раньше): {descriptions_sections_page.difference(descriptions_sections)}")
        print(f"Кол. разделов: {len(descriptions_sections_page)}")
        print('-' * 20)
        # ---

        descriptions_sections = descriptions_sections.union(descriptions_sections_page)
        # ---
        count_iteration += 1
        # ---
    return descriptions_sections


def get_descriptions_sections_page(src):
    descriptions_sections_page = set()

    soup = BeautifulSoup(src, "lxml")

    table_info = soup.find("h3", text=re.compile("Сведения о документе")).find_parent('div', class_="book-info")
    rows_info = table_info.find_all('div', class_="book-info-table")

    # Начинаем с второй строчки таблицы т.к в первой не стандартный формат
    # И данные в ней есть выше на странице (Заглавие), а (Вид документа) нам и не нужен т.к все рукописи
    for row_info in rows_info[1:]:
        section_name = row_info.find('div').find('div')
        section_data = section_name.find_next()

        descriptions_sections_page.add(section_name.text.strip())

    return descriptions_sections_page


def main():
    # -----
    # """Код уже отработал создано два файла в папке "folder_links_pages":
    # "links_pages_true.json" - рукописи, дата которых ниже 16 века (по мнению сайта!)
    # "links_pages_maybe.json" - рукописи у которых спорная дата, где есть переход Н: XVI-XVII или 1597-1603
    # """
    # if not os.path.exists("data/folder_links_pages"):
    #     os.mkdir("data/folder_links_pages")
    #
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36",
    # }
    #
    # write_file_links_pages("https://kp.rusneb.ru/item/thematicsection/slavic-manuscripts", headers)
    # -----

    # -----
    # """Код не запускать он уже отработал файл готов с всеми возможными разделами описания
    # Название файла: "descriptions_sections_names.json"
    # """
    # descriptions_sections = get_count_descriptions_sections(headers)
    # descriptions_sections = list(descriptions_sections)
    # # ---
    # print(f"Общее кол. разделов описания: {len(descriptions_sections)}")
    # # ---
    # with open("data/descriptions_sections_names.json", "w", encoding="utf-8") as file:
    #     json.dump(descriptions_sections, file, indent=4, ensure_ascii=False)
    # -----
    pass


if __name__ == "__main__":
    main()
