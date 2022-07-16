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


def collect_data_books_info(headers):
    with open('data/links_pages.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # -----
    if not os.path.exists("data/pages_books"):
        os.mkdir("data/pages_books")
    # -----

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f'data/data_books_info/books_info_{cur_time}.json', "w", encoding='utf-8') as json_file:
        pass

    # -----
    count_iteration = 0
    # -----
    for link_content in data[:3]:

        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {link_content['title']}")
        # ---

        # -----
        """Получаем src страницы (содержимое) (html)"""
        title_book_eng_for_link = re_functions.get_title_book_eng_for_link(link_content["link"])
        if not title_book_eng_for_link:
            title_book_eng_for_link = f"book_{count_iteration}"

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
                with open(f"data/pages_books/{title_book_eng_for_link}.html", 'w', encoding='utf-8') as file:
                    file.write(req.text)

        with open(f"data/pages_books/{title_book_eng_for_link}.html", encoding='utf-8') as file:
            src = file.read()
        # -----

        data_book_info = ""

        collect_data_book_info(src=src)

        with open(f'data/data_books_info/books_info_{cur_time}.json', "a", encoding="utf-8") as json_file:
            json.dump(data_book_info, json_file, indent=4, ensure_ascii=False)

        # -----
        count_iteration += 1
        # -----

        # ---
        print(*["-" * 20] * 3, sep='\n')
        # ---


def collect_data_book_info(src):
    soup = BeautifulSoup(src, "lxml")


def main():
    if not os.path.exists("data/data_books_info"):
        os.mkdir("data/data_books_info")

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36",
    }

    collect_data_books_info(headers)


if __name__ == "__main__":
    main()
