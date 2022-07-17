import os
import datetime
import time
import json
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re

import re_functions_for_collect_data_books_info as re_functions


def manager_page_book_html(link_content, headers):
    # -----
    """Получаем src страницы (содержимое) (html)"""
    title_book_eng_for_link = re_functions.get_title_book_eng_for_link(link_content["link"])
    # if not title_book_eng_for_link:
    #     title_book_eng_for_link = f"book_{count_iteration}"
    if not os.path.exists(f"data/pages_books/{title_book_eng_for_link}.html"):

        try:
            req = requests.get(link_content["link"], headers)
            # просто чтобы не забыть
            # response.status_code == 200:
            req.encoding = 'utf-8'
            time.sleep(3)
            req.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            # ---
            print(f'[my_ERROR] Не рабочая ссылка? {http_err}')
            # ---
            raise http_err

            # # -----
            # '''Код на случай если нужно будет продолжат работу'''
            # # -----
            # count_iteration += 1
            # # -----
            #
            # # ---
            # print(*["-" * 20] * 3, sep='\n')
            # # ---
            # continue
            # # -----

        except requests.ConnectionError as connect_err:
            # ---
            print(f'[my_ERROR] НЕТ ИНТЕРНЕТА {connect_err}')
            # ---
            raise connect_err

        except Exception as err:
            # ---
            print(f'[my_ERROR] любая ошибка: {err}')
            # ---
            raise err
        else:
            # write_page_book_html
            with open(f"data/pages_books/{title_book_eng_for_link}.html", 'w', encoding='utf-8') as file:
                file.write(req.text)


def manager_pages_books_html():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36",
    }

    with open('data/links_pages.json', encoding='utf-8') as json_file:
        links_content = json.load(json_file)

    for link_content in links_content:
        manager_page_book_html(link_content, headers)


def write_data_book_json_book(data_book: dict, title_book_eng_for_link: str, cur_time: str):
    with open(f'data/data_books/books/{title_book_eng_for_link}/{cur_time}/collect_data_book.json', "w",
              encoding="utf-8") as json_file:
        json.dump(data_book, json_file, indent=4, ensure_ascii=False)


def write_data_book_json_books(data_book: dict, cur_time: str, count_iteration: int):
    with open(f'data/data_books/all_books/{cur_time}/collect_data_books.json', "a",
              encoding="utf-8") as json_file:
        if count_iteration != 0:
            json_file.write(',\n')
        json.dump(data_book, json_file, indent=4, ensure_ascii=False)


def read_data_book_json(title_book_eng_for_link: str, cur_time: str):
    with open(
            f'data/data_books/books/{title_book_eng_for_link}/{cur_time}/collect_data_book.json',
            encoding='utf-8') as json_file:
        data_book = json.load(json_file)

    return data_book


def collect_data_book_title(soup):
    try:
        title = soup.find('div', class_="hero-content").find('h1').text.strip()
    except AttributeError as attribute_err:
        print(f"[my_ERROR]: 'title' {attribute_err}")
        return {}
    else:
        return {'title': title}


def collect_data_book_date(soup):
    try:
        date = soup.find('div', text=re.compile(r"Дата издания\/создания")).find_next_sibling('div').text.strip()
    except AttributeError as attribute_err:
        print(f"[my_ERROR] 'date': {attribute_err}")
        return {}
    else:
        return {'date': date}


def collect_data_book_sheets_number(soup):
    try:
        sheets_number = soup.find('div', text=re.compile(r"Объем издания")).find_next_sibling('div').text.strip()
    except AttributeError as attribute_err:
        print(f"[my_ERROR]: 'sheets_number' {attribute_err}")
        return {}
    else:
        return {'sheets_number': sheets_number}


def collect_data_book_owner(soup):
    try:
        owner = soup.find('div', text=re.compile(r"Владелец")).find_next_sibling('div').text.strip()
    except AttributeError as attribute_err:
        print(f"[my_ERROR]: 'owner' {attribute_err}")
        return {}
    else:
        return {'owner': owner}


def collect_data_book_info(soup):
    data_book_info = {}

    soup_table_info = soup.find("h3", text=re.compile('Сведения о документе')).find_parent('div',
                                                                                           class_="book-info")

    data_book_info.update(collect_data_book_title(soup))
    data_book_info.update(collect_data_book_date(soup_table_info))
    data_book_info.update(collect_data_book_sheets_number(soup_table_info))
    data_book_info.update(collect_data_book_owner(soup_table_info))

    return data_book_info


def manager_collect_data_book(page_html, cur_time, title_book_eng_for_link):
    if not os.path.exists(f"data/data_books/books/{title_book_eng_for_link}"):
        os.mkdir(f"data/data_books/books/{title_book_eng_for_link}")
    if not os.path.exists(f"data/data_books/books/{title_book_eng_for_link}/{cur_time}"):
        os.mkdir(f"data/data_books/books/{title_book_eng_for_link}/{cur_time}")

    with open(f"data/pages_books/{page_html}", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    data_book = {}
    data_book['title_book_eng_for_link'] = title_book_eng_for_link
    data_book['info'] = collect_data_book_info(soup)

    write_data_book_json_book(data_book, title_book_eng_for_link, cur_time)


def manager_collect_data_books(pages_html, cur_time):
    if not os.path.exists("data/data_books"):
        os.mkdir("data/data_books")
    if not os.path.exists("data/data_books/all_books"):
        os.mkdir("data/data_books/all_books")
    if not os.path.exists("data/data_books/books"):
        os.mkdir("data/data_books/books")
    if not os.path.exists(f"data/data_books/all_books/{cur_time}"):
        os.mkdir(f"data/data_books/all_books/{cur_time}")

    with open(f'data/data_books/all_books/{cur_time}/collect_data_books.json', "w",
              encoding="utf-8") as json_file:
        json_file.write('[\n')
    # -----
    count_iteration = 0
    # -----
    for page_html in pages_html[:2]:
        title_book_eng_for_link = re_functions.get_file_name_not_extension(page_html)
        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {title_book_eng_for_link}")
        # ---

        manager_collect_data_book(page_html, cur_time, title_book_eng_for_link)

        data_book = read_data_book_json(title_book_eng_for_link, cur_time)

        write_data_book_json_books(data_book, cur_time, count_iteration)

        # -----
        count_iteration += 1
        # -----
        # ---
        print(*["-" * 20] * 3, sep='\n')
        # ---

    with open(f'data/data_books/all_books/{cur_time}/collect_data_books.json', "a",
              encoding="utf-8") as json_file:
        json_file.write('\n]')


def main():
    # manager_pages_books_html()

    pages_html = os.listdir('data/pages_books')
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    manager_collect_data_books(pages_html, cur_time)


if __name__ == "__main__":
    main()
